Name:           steamos-base-files
Version:        2.49
Release:        1%{?dist}
Summary:        Files specific to the SteamOS distribution

License:        BSD
URL:            http://store.steampowered.com/steamos/
Source0:        http://repo.steampowered.com/steamos/pool/main/s/%{name}/%{name}_%{version}.tar.gz
# Modified script for Fedora, inspired by original steamos-update package
Source1:        steamos-update

BuildArch:      noarch

Requires:       glib2
Requires:       polkit-pkla-compat
Requires:       sudo

%description
This package contains files specific to the SteamOS experience, particularly
systemd login policies and additional commands.

%prep
%setup -q
cp %{SOURCE1} .%{_bindir}/

%if 0%{?fedora} == 21 || 0%{?rhel} == 7
sed -i -e 's/dnf/yum/g' .%{_bindir}/steamos-update
%endif    

%install
mkdir -p %{buildroot}%{_bindir}/
install -p -m755 .%{_bindir}/* \
    %{buildroot}%{_bindir}/

rm -f %{buildroot}%{_bindir}/{chrony-shutdown,steamos-autorepair.sh}

mkdir -p %{buildroot}%{_sysconfdir}/sudoers.d/
install -p -m644 .%{_sysconfdir}/sudoers.d/* \
    %{buildroot}%{_sysconfdir}/sudoers.d/

mkdir -p %{buildroot}%{_datadir}/glib-2.0/schemas/
install -p -m644 .%{_datadir}/glib-2.0/schemas/10_steam.gschema.override \
    %{buildroot}%{_datadir}/glib-2.0/schemas/

mkdir -p %{buildroot}%{_sysconfdir}/polkit-1/localauthority.conf.d/
install -p -m644 .%{_sysconfdir}/polkit-1/localauthority.conf.d/51-steamos-admin.conf \
    %{buildroot}%{_sysconfdir}/polkit-1/localauthority.conf.d/
    
mkdir -p %{buildroot}%{_sharedstatedir}/polkit-1/localauthority/50-local.d/
install -p -m644 .%{_sharedstatedir}/polkit-1/localauthority/50-local.d/* \
    %{buildroot}%{_sharedstatedir}/polkit-1/localauthority/50-local.d/

mkdir -p %{buildroot}%{_sysconfdir}/skel/Desktop
install -p -m644 .%{_sysconfdir}/skel/Desktop/* \
    %{buildroot}%{_sysconfdir}/skel/Desktop/

mkdir -p %{buildroot}%{_sysconfdir}/skel/.local/share/applications/
install -p -m644 .%{_sysconfdir}/skel/.local/share/applications/* \
    %{buildroot}%{_sysconfdir}/skel/.local/share/applications/

# This SteamOS "variant" is not supported by Valve
find %{buildroot} -name "*bugreport*" -delete

%files
%doc debian/copyright debian/changelog
%{_bindir}/alienware_wmi_control.sh
%{_bindir}/returntosteam.sh
%{_bindir}/steamkillall.sh
%{_bindir}/steamos-update
%{_bindir}/steam_serialnumber.sh
%{_datadir}/glib-2.0/schemas/*
%{_sharedstatedir}/polkit-1/localauthority/50-local.d/*
%{_sysconfdir}/polkit-1/localauthority.conf.d/*
%{_sysconfdir}/skel/Desktop
%{_sysconfdir}/skel/.local
%{_sysconfdir}/sudoers.d/*

%changelog
* Sat Oct 31 2015 Simone Caronni <negativo17@gmail.com> - 2.49-1
- Update to version 2.49.
- Use dnf in steamos-update for Fedora 22+.
- Add skeleton files for user profiles and additional scripts.

* Fri Jul 31 2015 Simone Caronni <negativo17@gmail.com> - 2.39-1
- Update to 2.39.

* Sun Jun  8 2014 Simone Caronni <negativo17@gmail.com> - 2.30-1
- First build.
