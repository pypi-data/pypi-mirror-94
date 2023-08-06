#!/usr/bin/env python3

import urllib.parse
import socket
import re
import sys
import codecs
import cgi
import os
import os.path
import datetime
import base64
import hashlib
import io

# https://www.pyopenssl.org/ Python standard library has the "ssl"
# module but PyOpenSSL offers more features.
import OpenSSL

from Agunua.urltinkering import urlmerge, uri_to_iri,iri_to_uri
from Agunua.utils import validate_hostname,format_x509_name

class GeminiException(Exception):
    pass

class NonGeminiUri(GeminiException):
    pass

class InvalidUri(GeminiException):
    pass

class WrongParameters(GeminiException):
    pass

class AlreadyIriOrWrongEncoding(GeminiException):
    pass

# Things you shouldn't touch
VERSION = "1.0"
GEMINI_PORT = 1965
BUFSIZE = 4096

# In uppercase, the defaults. Most can be changed when calling the constructor.
GET_CONTENT=False
PARSE_CONTENT=False
INSECURE = False
MAXSIZE = 2**20
MAXLINES = 1000
MAXDEPTH = 4 # Max redirections <gemini://gemini.circumlunar.space/docs/best-practices.gmi> suggests 5.
FOLLOW_REDIRECT = False
DEBUG = False
IRI = True
TOFU = os.path.join(os.environ["HOME"], ".agunua/fingerprints/") # If it is set to "" or None, we don't trust (no tofu).
FORCE_IPV4 = False
FORCE_IPV6 = False
SEND_SNI = True
ACCEPT_EXPIRED = False
BINARY = False

def read(session, maxsize=MAXSIZE):
    """Returns a generator, yields a binary buffer, the caller may have to
call decode() itself.
    """
    binary = False
    buffer = b""
    while True:
        if not binary:
            offset = None
            eol = buffer.find(b"\r\n")
            if eol == -1:
                eol = buffer.find(b"\n") # Accept raw \n because we're liberal.
                if eol != -1:
                    offset = 1
            else:
                offset = 2
            if offset is None:
                try:
                    buffer += session.recv(BUFSIZE)
                except (OpenSSL.SSL.ZeroReturnError, OpenSSL.SSL.SysCallError):
                    yield buffer
                    break
            else:
                binary = yield buffer[:eol]
                buffer = buffer[eol+offset:]
        else:
            try:
                buffer += session.recv(BUFSIZE)
                if maxsize is not None and maxsize > 0 and len(buffer) > maxsize:
                    yield buffer[0:maxsize]
                    break
            except (OpenSSL.SSL.ZeroReturnError, OpenSSL.SSL.SysCallError):
                yield buffer
                break

def parse_text(t, url=None):
    content = []
    b = io.StringIO(t)
    for l in b.readlines():
        content.append(l[:-1]) # Chop end-of-line
    return parse(content, url)

def parse(content, url=None):
    """Parse a gemtext (Gemini usual format) content (an array of lines)
and returns an array of the links it contains. If url is None, we
dont' handle relative links, and ignore them.
    """
    result = []
    in_prefor = False
    components = urllib.parse.urlparse(url)
    for l in content:
        if l[0:2] == "=>" and not in_prefor:
            l = re.sub("^\s*", "", l[2:]) # Strip leading spaces.
            s = re.split("[ \t]+", l, maxsplit=1)
            if len(s) == 2:
                (link, text) = s
            else:
                link = s[0] # Link without a text
                if re.search("^\s*$", link):
                    continue # gemini://gemini.conman.org/test/torture/0032
            try:
                link = uri_to_iri(link)
            except AlreadyIriOrWrongEncoding:
                pass
            except ValueError as e:
                pass # Ignore broken URLs
            try:
                components_link = urllib.parse.urlparse(link)
            except ValueError:
                continue # Ignore broken URLs                
            if components_link.scheme == "": # Relative link
                if url is not None:
                    # Unfortunately, Python's standard library's
                    # urllib.parse.urljoin does not work with non-HTTP
                    # URIs :-( So we have to do that ourselves. There
                    # is an interesting trick in
                    # <https://tildegit.org/solderpunk/gemini-demo-1>
                    # (replace gemini with http, join and replace
                    # back) but we preferred to reimplement.
                    result.append(urlmerge(url, link))
            elif components_link.scheme == "gemini" and link not in result: 
                result.append(link)
            else:
                pass # Ignore other URL schemes.
        elif l[0:3] == "```":
            in_prefor = not in_prefor
        else:
            pass # Ignore other line types (for instance, we don't care about headings such as #).
    return result

class GeminiUri():
    
    def __init__(self, url, insecure=INSECURE,
                 get_content=GET_CONTENT, parse_content=PARSE_CONTENT,
                 maxlines=MAXLINES, maxsize=MAXSIZE, binary=BINARY,
                 follow_redirect=FOLLOW_REDIRECT, iri=IRI, tofu=TOFU,
                 redirect_depth=0, force_ipv4=FORCE_IPV4,
                 force_ipv6=FORCE_IPV6, send_sni=SEND_SNI,
                 connect_to=None, accept_expired=ACCEPT_EXPIRED,
                 debug=DEBUG):
        """Note it does not enforce robots.txt. The caller has to do it.
        
        There are two categories of failures: invalid URLs
        (non-Gemini, syntax errors, etc) which raise an exception, and
        network issues (connection refused, etc), where you still get
        an object, but with network_success == False.

        WARNING: there is no timeout, so you risk being blocked for
        ever, for instance if the server is nasty and accepts
        connections but then never writes anything. The caller has to
        handle this, using alarm signals or stuff like that. An
        example is in the command-line client,
        agunua.py. (Implementing a timeout with PyOpenSSL is *hard*,
        see <https://github.com/pyca/pyopenssl/issues/168>.)

        If maxlines or maxsize are 0 or None, there is no limit.

        DEVELOPERS: if you add parameters to this constructor, do not
        forget to add them also in the recursive call later, and of
        course to document it in README.md.

        """
        # Consistency checks
        if force_ipv4 and force_ipv6:
            raise WrongParameters("Force IPv4 or force IPv6 but not both")
        if binary and parse_content:
            raise WrongParameters("Parsing content is not compatible with binary retrieval")
        self.url = url
        self.insecure = insecure
        self.network_success = False
        self.ip_address = None
        self.status_code = None
        self.meta = None
        self.links = None # An array. If empty, means there was no
                          # links. If None, means the file was not
                          # gemtext, or was not parsed.
        self.error = "No error"
        self.payload = None
        do_idn = False
        try:
            components = urllib.parse.urlparse(url)
        except ValueError: # Invalid URL 
            raise InvalidUri()
        if components.scheme != "gemini":
            raise NonGeminiUri(components.scheme)
        host = components.hostname
        if connect_to is None:
            host_used = host
        else:
            host_used = connect_to
        if iri:
            try:
                ascii_host = codecs.encode(host, encoding="idna").decode()
            except UnicodeError:
                raise InvalidUri()
            if ascii_host != host:
                do_idn = True
            else:
                ascii_host = host
        try:
            port = components.port
        except ValueError: # I've seen strange things.
            raise InvalidUri("Invalid port in URI")
        if port is None:
            port = GEMINI_PORT
        if port != GEMINI_PORT:
            tport = ":%s" % port
        else:
            tport = ""
        if components.query != "":
            query = "%s" % components.query
        else:
            query = ""
        if parse_content:
            get_content = True
        try:
            # Python handles punycoding (for IDN) if necessary
            addrinfo_list = socket.getaddrinfo(host_used, port)
        except socket.gaierror:
            self.error = "Name %s not known or invalid" % host
            return 
        addrinfo_set = { (addrinfo[4], addrinfo[0]) for addrinfo in addrinfo_list }
        tested_addresses = 0
        for (addr, family) in addrinfo_set:
            if force_ipv4 and family == socket.AddressFamily.AF_INET6:
                continue
            if force_ipv6 and family == socket.AddressFamily.AF_INET:
                continue
            sock = socket.socket(family, socket.SOCK_STREAM)
            context = OpenSSL.SSL.Context(OpenSSL.SSL.TLSv1_2_METHOD)
            if self.insecure: 
                # Many Gemini capsules have only a self-signed certificate
                context.set_verify(OpenSSL.SSL.VERIFY_NONE, lambda *x: True)
            else:
                context.set_default_verify_paths()
                context.set_verify(OpenSSL.SSL.VERIFY_PEER | OpenSSL.SSL.VERIFY_FAIL_IF_NO_PEER_CERT | \
                               OpenSSL.SSL.VERIFY_CLIENT_ONCE,
                                   lambda conn, cert, errno, depth, preverify_ok: preverify_ok)
            session = OpenSSL.SSL.Connection(context, sock)
            if send_sni:
                session.set_tlsext_host_name(ascii_host.encode()) # Server Name Indication (SNI)
            try:
                tested_addresses += 1
                if debug:
                    print("DEBUG: trying to connect to %s ..." % str(addr), file=sys.stderr)
                try:
                    session.connect(addr)
                except OSError as e:
                    self.error = "Cannot connect to host %s: %s" % (addr, e)
                    if debug:
                        print("DEBUG: failed: %s" % self.error, file=sys.stderr)
                    continue
                try:
                    sock.setblocking(True) # Long-standing issue https://github.com/pyca/pyopenssl/issues/168
                    session.do_handshake()
                except OpenSSL.SSL.Error as e:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    self.error = "TLS handshake error %s: problem in the certificate? \"%s\"" % (exc_type, exc_value)
                    if debug:
                        print("DEBUG: failed: %s" % self.error, file=sys.stderr)
                    continue
                cert = session.get_peer_certificate()
                if tofu is not None and tofu != "":
                    self.hasher = hashlib.sha256()
                if not insecure:
                    valid = validate_hostname(ascii_host, cert, iri)
                    if not valid:
                        self.error = "Name %s not in certificate" % ascii_host
                        continue
                if not accept_expired:
                    if cert.has_expired():
                        self.error = "Certificate has expired"
                        continue
                if tofu is not None and tofu != "":
                    os.makedirs(tofu, exist_ok = True)
                    publickey = cert.get_pubkey()
                    self.hasher.update(OpenSSL.crypto.dump_publickey(OpenSSL.crypto.FILETYPE_ASN1,
                                                                publickey))
                    digest = self.hasher.digest()
                    self.keystring = base64.standard_b64encode(digest).decode()
                    pkeyfile_name = os.path.join(tofu, ascii_host + tport)
                    try:
                        pkeyfile = open(pkeyfile_name, "r")
                        old_key = pkeyfile.read()
                        if self.keystring != old_key:
                            self.error = "Former public key at %s was %s, new one is %s. If the change is legitimate, delete %s " % \
                                              (addr, old_key, self.keystring, pkeyfile_name)
                            continue
                    except FileNotFoundError:
                        # Trust on First Time
                        pass
                    pkeyfile = open(pkeyfile_name, "w")
                    pkeyfile.write(self.keystring)
                    pkeyfile.close()
                uri = urllib.parse.urlunsplit(("gemini", ascii_host + tport, components.path , query, None))
                request = iri_to_uri(uri) + "\r\n" # We
                # do not send the fragment to the server
                if debug:
                    print("DEBUG: connected with %s" % str(addr))
                session.send(request.encode())
                reader = read(session, maxsize=maxsize)
                try:
                    header = next(reader).decode("utf-8")
                except StopIteration:
                    self.error = "No header line"
                    continue
                if len(header) <= 3:
                    self.error = "Short header"
                    continue
                self.header = header
                # The Gemini protocol has no equivalent of HTTP
                # Content-Length
                # <https://gemini.circumlunar.space/docs/faq.html> or
                # EPP or DNS explicit lengths. The only way to read
                # everything is to go until EOF exception.
                self.status_code = header[0:2]
                if not re.search("^[0-9]{2}$", self.status_code):
                    self.error = "Wrong status code \"%s\"" % self.status_code
                    continue
                if header[2] != " ": # gemini://egsam.glv.one/3.1.gmi
                    self.error = "Erroneous header line"
                    continue
                self.meta = header[3:]
                if self.status_code == "20":
                    mtype, mime_opts = cgi.parse_header(self.meta)
                    self.mediatype = mtype
                    self.lang = ""
                    self.charset = ""
                    for key in mime_opts:                                                                       
                        if key == "lang":
                            self.lang = mime_opts["lang"].lower()
                        elif key == "charset":                                                                              
                            self.charset = mime_opts["charset"].lower()
                    if self.charset == "":
                        charset = "utf-8"
                    else:
                        charset = self.charset
                    content = []
                    self.binary = binary
                    if get_content:
                        if not binary and mtype.startswith("text/"):
                            self.payload = ""
                            i = 0
                            while True:
                                if maxlines is not None and maxlines > 0 and i > maxlines:
                                    break
                                try:
                                    l = next(reader).decode(charset)
                                    content.append(l)
                                    i += 1
                                    self.payload += (l + "\r\n")
                                except StopIteration:
                                    break
                                except UnicodeDecodeError:
                                    # Retry in binary (requires to disable parse_content)
                                    self.__init__(url,
                                          get_content=get_content,
                                          parse_content=False,
                                          maxlines=maxlines,
                                          maxsize=maxsize,
                                          binary=True,
                                          insecure=insecure,
                                          force_ipv4=force_ipv4,
                                          force_ipv6=force_ipv6,
                                          send_sni=send_sni,
                                          connect_to=connect_to,
                                          accept_expired=accept_expired,
                                          tofu=tofu, debug=debug,
                                          follow_redirect=follow_redirect,
                                          redirect_depth=redirect_depth+1)
                                    self.binary = True
                                    self.error = "Announced charset %s does not match the content" % charset
                                    break
                                except LookupError:
                                    # Retry in binary (requires to disable parse_content)
                                    self.__init__(url,
                                          get_content=get_content,
                                          parse_content=False,
                                          maxlines=maxlines,
                                          maxsize=maxsize,
                                          binary=True,
                                          insecure=insecure,
                                          force_ipv4=force_ipv4,
                                          force_ipv6=force_ipv6,
                                          send_sni=send_sni,
                                          connect_to=connect_to,
                                          accept_expired=accept_expired,
                                          tofu=tofu, debug=debug,
                                          follow_redirect=follow_redirect,
                                          redirect_depth=redirect_depth+1)
                                    self.binary = True
                                    self.error = "Announced charset %s is unknown to me" % charset
                                    self.payload = ""
                                    break
                        else:
                            self.payload = reader.send(True)
                            while True:
                                try:
                                    d = next(reader)
                                    self.payload += d
                                except StopIteration:
                                    break  
                self.network_success = True
                if self.status_code == "30" or self.status_code == "31":
                    if follow_redirect:
                        if redirect_depth <= MAXDEPTH:
                            self.__init__(urlmerge(url, self.meta),
                                          get_content=get_content,
                                          parse_content=parse_content,
                                          maxlines=maxlines,
                                          maxsize=maxsize,
                                          binary=binary,
                                          insecure=insecure,
                                          force_ipv4=force_ipv4,
                                          force_ipv6=force_ipv6,
                                          send_sni=send_sni,
                                          connect_to=connect_to,
                                          accept_expired=accept_expired,
                                          tofu=tofu, debug=debug,
                                          follow_redirect=follow_redirect,
                                          redirect_depth=redirect_depth+1)
                            return
                        else:
                            self.network_success = False
                            self.error = "Too many redirects"
                elif self.status_code == "20":
                    if parse_content and self.mediatype == "text/gemini":
                        self.links = parse(content, url)
                session.shutdown()
                session.close()
                break
            except (ConnectionRefusedError, TimeoutError) as e:  # Or "isinstance(err, (TimeoutError, socket.timeout))" ?
                self.error = "%s failed because of \"%s\"" % (addr, e)
                continue # Try another address
        if tested_addresses == 0:
            self.error = "No IP address available"
        self.ip_address = addr[0]
        if self.network_success:
            self.issuer = format_x509_name(cert.get_issuer()) 
            self.subject = format_x509_name(cert.get_subject())
            self.cert_not_after = datetime.datetime.strptime(cert.get_notAfter().decode(), "%Y%m%d%H%M%SZ")
            self.cert_not_before = datetime.datetime.strptime(cert.get_notBefore().decode(), "%Y%m%d%H%M%SZ")
            self.cert_algo = cert.get_signature_algorithm().decode()
            self.cert_key_type = cert.get_pubkey().type() 
            self.cert_key_size = cert.get_pubkey().bits()
            if self.status_code == "20" and get_content:
                self.size = len(self.payload)

    def __str__(self):
        if self.network_success:
            return("%s / %s OK: code %s" % (self.url, self.ip_address, self.status_code))
        else:
            return("%s FAIL: \"%s\"" % (self.url, self.error))
