# TODO
# - bconds for modules as these are statically linked in
# - initscript
Summary:	high perfomance http and reverse proxy server
Name:		nginx
Version:	0.1.41
Release:	0.3
Epoch:		0
License:	ASIS
Group:		Applications
Source0:	http://sysoev.ru/nginx/%{name}-%{version}.tar.gz
# Source0-md5:	475ae6d06dd61dc93fdcaf1069d7db21
Patch0:		%{name}-DESTDIR.patch
URL:		http://sysoev.ru/en/
%if %{with initscript}
BuildRequires:	rpmbuild(macros) >= 1.228
Requires(post,preun):	rc-scripts
Requires(post,preun):	/sbin/chkconfig
%endif
BuildRequires:	pcre-devel
BuildRequires:	openssl-devel
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir /etc/%{name}

%description
high perfomance http and reverse proxy server.

%prep
%setup -q
%patch0 -p1

%build
# NB: not autoconf generated configure
./configure \
	--prefix=%{_prefix} \
	--sbin-path=%{_sbindir}/%{name} \
	--conf-path=%{_sysconfdir}/%{name}.conf \
	--error-log-path=%{_localstatedir}/log/%{name}/error.log \
	--pid-path=%{_localstatedir}/run/%{name}.pid \
	--user=nobody \
	--group=nobody \
	--with-threads \
	--with-rtsig_module \
	--with-select_module \
	--with-poll_module \
	--with-http_ssl_module \
	--http-log-path=%{_localstatedir}/log/%{name}/access.log \
	--http-client-body-temp-path=%{_localstatedir}/cache/%{name}/client_body_temp \
	--http-proxy-temp-path=%{_localstatedir}/cache/%{name}/proxy_temp \
	--http-fastcgi-temp-path=%{_localstatedir}/cache/%{name}/fastcgi_temp \
	--with-imap \
	--with-cc="%{__cc}" \
	--with-cc-opt="%{rpmcflags}" \
	--with-ld-opt="%{rpmldflags}" \
	%{?debug:--with-debug}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_sysconfdir}/*.default
rm -rf $RPM_BUILD_ROOT%{_prefix}/html

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with initscript}
%post
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del %{name}
fi
%endif

%files
%defattr(644,root,root,755)
%doc CHANGES LICENSE README html/index.html conf/nginx.conf
%doc %lang(ru) CHANGES.ru
%dir %{_sysconfdir}
%{_sysconfdir}/koi-win
%{_sysconfdir}/mime.types
%{_sysconfdir}/nginx.conf
%attr(755,root,root) %{_sbindir}/nginx