%define gimp_api_version 2.0

Summary:	G'MIC extends GIMP's retouching software capabilities with additional filters and effects
Name:		gmic
Version:	1.4.5.2
Release:	%mkrel 2
License:	CeCILL
Group:		Graphics
Url:		http://gmic.sourceforge.net/
Source0:	http://downloads.sourceforge.net/gmic/%{name}_%{version}.tar.gz
Patch0:		gmic_1.4.5.2-link.patch
Requires:	gimp
BuildRequires:	gimp-devel fftw3-devel graphicsmagick graphicsmagick-devel
BuildRequires:	opencv-devel OpenEXR-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
G'MIC stands for GREYC's Magic Image Converter. This project aims to define a
minimal but powerful script language (G'MIC) dedicated to the design of image
processing pipelines, provide an interpreter of this language (in C++),
distributed as an open-source module/library embeddable in third-party
applications and propose two tools embedding this interpreter: The command-line
executable gmic to use the G'MIC framework from a shell, and the interactive
plug-in gmic_gimp to bring G'MIC capabilities to the image retouching software
GIMP.

G'MIC is focused on the design of complex pipelines for converting,
manipulating, filtering and visualizing generic 1d/2d/3d multi-spectral image
datasets. Of course, it is able to manage color images, but also more complex
data as image sequences or 3d volumetric datasets.

G'MIC is an open framework : it is possible to extend the proposed default
language with custom G'MIC-written commands, defining thus new image filters or
effects.

%prep
%setup -q
%patch0 -p0 -b .link

%build
%configure2_5x
%make

%install
rm -rf %{buildroot}
%makeinstall_std

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README AUTHORS COPYING NEWS
%{_bindir}/gmic
%{_libdir}/gimp/%{gimp_api_version}/plug-ins/gmic_gimp
%{_mandir}/*/*
%{_sysconfdir}/bash_completion.d/gmic
