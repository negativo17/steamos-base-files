# Omit by default. It does the following for every user on the system:
# - disables screensaver
# - suspend with power button
# - changes background
# - scales text to 1.5
#
#global _with_gschema 1

Name:           steamos-base-files
Version:        2.58
Release:        1%{?dist}
Summary:        Files specific to the SteamOS distribution
License:        BSD
URL:            http://store.steampowered.com/steamos/

Source0:        http://repo.steamstatic.com/steamos/pool/main/s/%{name}/%{name}_%{version}.tar.xz
Source1:        50-poweroff.pkla
Patch0:         steamos-base-files-2.58-sudoers.patch

BuildArch:      noarch

%{?_with_ffmpeg:
Requires:       glib2
Requires:       steamos-backgrounds
}

Requires:       polkit-pkla-compat
Requires:       steamos-compositor
Requires:       sudo

%description
This package contains files specific to the SteamOS experience.

%prep
%autosetup -p1
cp %{SOURCE1} .%{_sharedstatedir}/polkit-1/localauthority/50-local.d/

%install
mkdir -p %{buildroot}%{_bindir}/
install -p -m755 .%{_bindir}/* %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{_sysconfdir}/sudoers.d/
install -p -m644 .%{_sysconfdir}/sudoers.d/* \
    %{buildroot}%{_sysconfdir}/sudoers.d/

%{?_with_ffmpeg:
mkdir -p %{buildroot}%{_datadir}/glib-2.0/schemas/
install -p -m644 .%{_datadir}/glib-2.0/schemas/10_steam.gschema.override \
    %{buildroot}%{_datadir}/glib-2.0/schemas/
}

mkdir -p %{buildroot}%{_sharedstatedir}/polkit-1/localauthority/50-local.d/
install -p -m644 .%{_sharedstatedir}/polkit-1/localauthority/50-local.d/* \
    %{buildroot}%{_sharedstatedir}/polkit-1/localauthority/50-local.d/

mkdir -p %{buildroot}%{_sysconfdir}/polkit-1/localauthority.conf.d/
install -p -m644 .%{_sysconfdir}/polkit-1/localauthority.conf.d/51-steamos-admin.conf \
    %{buildroot}%{_sysconfdir}/polkit-1/localauthority.conf.d/

rm -f %{buildroot}%{_bindir}/{chrony-shutdown,steamos-autorepair.sh,bugreport.sh}
rm -f %{buildroot}%{_sysconfdir}/sudoers.d/valve-bugreporter

%files
%doc debian/copyright debian/changelog
%{_bindir}/alienware_wmi_control.sh
%{_bindir}/returntosteam.sh
%{_bindir}/steamkillall.sh
%{_bindir}/steam_serialnumber.sh
%{?_with_ffmpeg:
%{_datadir}/glib-2.0/schemas/10_steam.gschema.override
}
%{_sharedstatedir}/polkit-1/localauthority/50-local.d/10-network-manager.pkla
%{_sharedstatedir}/polkit-1/localauthority/50-local.d/20-all-user-stop.pkla
%{_sharedstatedir}/polkit-1/localauthority/50-local.d/30-all-user-restart.pkla
%{_sharedstatedir}/polkit-1/localauthority/50-local.d/40-all-user-datetime.pkla
%{_sharedstatedir}/polkit-1/localauthority/50-local.d/50-poweroff.pkla
%{_sysconfdir}/polkit-1/localauthority.conf.d/51-steamos-admin.conf
%{_sysconfdir}/sudoers.d/steam_serialnumber
%{_sysconfdir}/sudoers.d/alienware_wmi_control

%changelog
* Sun Jan 27 2019 Simone Caronni <negativo17@gmail.com> - 2.58-1
- Update to 2.58.
- Update SPEC file.
- Move power off PolicyKit file from steamos-compositor.

* Sat Apr 15 2017 Simone Caronni <negativo17@gmail.com> - 2.54-1
- Update to 2.54.
- Require steamos-backgrounds for main session.
- Remove steamos-update script.

* Fri Apr 01 2016 Simone Caronni <negativo17@gmail.com> - 2.51-1
- Update to 2.51.

* Sat Oct 31 2015 Simone Caronni <negativo17@gmail.com> - 2.49-1
- Update to version 2.49.
- Use dnf in steamos-update for Fedora 22+.
- Add skeleton files for user profiles and additional scripts.

* Fri Jul 31 2015 Simone Caronni <negativo17@gmail.com> - 2.39-1
- Update to 2.39.

* Sun Jun  8 2014 Simone Caronni <negativo17@gmail.com> - 2.30-1
- First build.
