Name:       acpid

Summary:    ACPI Event Daemon
Version:    2.0.14
Release:    1
Group:      System/Daemons
License:    GPLv2+ and BSD
ExclusiveArch:  ia64 x86_64 %{ix86}
URL:        https://github.com/sailfishos/acpid2
Source0:    %{name}-%{version}.tar.gz
Source1:    acpid.video.conf
Source2:    acpid.power.conf
Source3:    acpid.power.sh
Source4:    acpid.lid.conf
Source5:    acpid.lid.sh
Source6:    acpid.battery.sh
Source7:    acpid.battery.conf
Source8:    acpid.ac.conf
Source9:    acpid-start-script
Source10:    acpid.start.sh
Source11:    acpid.service
Source12:    acpid.conf
Patch0:     acpid-2.0.9-makefile.patch
Patch1:     acpid-2.0.14-bugfix-incorrect-sizeof-usage-for-memset.patch
Requires:   systemd
Requires(preun): systemd
Requires(post): systemd
Requires(postun): systemd

%description
acpid is a daemon that dispatches ACPI events to user-space programs.

%package extra-docs
Summary:    sample docs and sample scripts for apcid
Group:      Documentation
Requires:   %{name} = %{version}-%{release}

%description extra-docs
Extra sample docs and scripts for acpid.


%prep
%setup -q -n %{name}-%{version}/%{name}

# acpid-2.0.9-makefile.patch
%patch0 -p1
# acpid-2.0.14-bugfix-incorrect-sizeof-usage-for-memset.patch
%patch1 -p1
# This binary is unintentionally present in older revisions in the git repo.
# Dist tarball have not contained it - drop it.
rm -f kacpimon/kacpimon

%build
make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/acpi/events
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/acpi/actions
mkdir -p $RPM_BUILD_ROOT%{_datadir}/acpi
chmod 755 $RPM_BUILD_ROOT%{_sysconfdir}/acpi/events
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/acpi/ac.d
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/acpi/battery.d
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/acpi/start.d
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/pm/sleep.d
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/acpi-support
mkdir -p $RPM_BUILD_ROOT/%{_lib}/systemd/system
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/acpi/events/videoconf
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/acpi/events/powerconf
install -m 755 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/acpi/actions/power.sh
install -m 644 %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/acpi/events/lidconf
install -m 755 %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/acpi/actions/lid.sh
install -m 755 %{SOURCE6} $RPM_BUILD_ROOT%{_sysconfdir}/acpi/actions/battery.sh
install -m 644 %{SOURCE7} $RPM_BUILD_ROOT%{_sysconfdir}/acpi/events/batteryconf
install -m 644 %{SOURCE8} $RPM_BUILD_ROOT%{_sysconfdir}/acpi/events/acconf
install -m 755 %{SOURCE9} $RPM_BUILD_ROOT%{_sbindir}/acpid-start-script
install -m 755 %{SOURCE10} $RPM_BUILD_ROOT%{_sysconfdir}/acpi/actions/start.sh
install -D -m 644 %{SOURCE11} $RPM_BUILD_ROOT/%{_lib}/systemd/system/acpid.service
install -D -m 644 %{SOURCE12} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/acpid

mkdir -p %{buildroot}/%{_lib}/systemd/system/multi-user.target.wants
ln -s ../acpid.service %{buildroot}/%{_lib}/systemd/system/multi-user.target.wants/acpid.service

%preun
if [ "$1" -eq 0 ]; then
systemctl stop acpid.service
fi

%post
systemctl daemon-reload
systemctl reload-or-try-restart acpid.service

%postun
systemctl daemon-reload

%files
%defattr(-,root,root,-)
%doc COPYING README Changelog TODO
%dir %{_sysconfdir}/acpi
%dir %{_sysconfdir}/acpi/events
%dir %{_sysconfdir}/acpi/actions
%dir %{_sysconfdir}/acpi/ac.d
%dir %{_sysconfdir}/acpi/battery.d
%dir %{_localstatedir}/lib/acpi-support
/%{_lib}/systemd/system/acpid.service
/%{_lib}/systemd/system/multi-user.target.wants/acpid.service
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/acpi/events/videoconf
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/acpi/events/powerconf
%config(noreplace) %attr(0755,root,root) %{_sysconfdir}/acpi/actions/power.sh
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/acpi/events/lidconf
%config(noreplace) %attr(0755,root,root) %{_sysconfdir}/acpi/actions/lid.sh
%config(noreplace) %attr(0755,root,root) %{_sysconfdir}/acpi/actions/battery.sh
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/acpi/events/batteryconf
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/acpi/events/acconf
%config(noreplace) %attr(0755,root,root) %{_sysconfdir}/acpi/actions/start.sh
%config(noreplace) %attr(0755,root,root) %{_sysconfdir}/sysconfig/acpid
%{_bindir}/acpi_listen
%{_sbindir}/acpid
%{_sbindir}/acpid-start-script
%{_mandir}/man8/acpid.8.gz
%{_mandir}/man8/acpi_listen.8.gz

%files extra-docs
%defattr(-,root,root,-)
%doc %{_defaultdocdir}/acpid/COPYING
%doc %{_defaultdocdir}/acpid/Changelog
%doc %{_defaultdocdir}/acpid/README
%doc %{_defaultdocdir}/acpid/TESTPLAN
%doc %{_defaultdocdir}/acpid/TODO
%doc %{_defaultdocdir}/acpid/samples/acpi_handler-conf
%doc %{_defaultdocdir}/acpid/samples/acpi_handler.sh
%doc %{_defaultdocdir}/acpid/samples/battery/battery-conf
%doc %{_defaultdocdir}/acpid/samples/battery/battery.sh
%doc %{_defaultdocdir}/acpid/samples/panasonic/ac_adapt.pl
%doc %{_defaultdocdir}/acpid/samples/panasonic/ac_adapter
%doc %{_defaultdocdir}/acpid/samples/panasonic/hotkey
%doc %{_defaultdocdir}/acpid/samples/panasonic/hotkey.pl
%doc %{_defaultdocdir}/acpid/samples/power
%doc %{_defaultdocdir}/acpid/samples/power.sh
%doc %{_defaultdocdir}/acpid/samples/powerbtn/powerbtn-conf
%doc %{_defaultdocdir}/acpid/samples/powerbtn/powerbtn.sh
%doc %{_defaultdocdir}/acpid/samples/powerbtn/powerbtn.sh.old
%doc %{_defaultdocdir}/acpid/COPYING
