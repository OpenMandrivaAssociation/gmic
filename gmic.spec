%define	major	2
%define	libname %mklibname %{name} %{major}
%define	develname %mklibname -d %{name}
%define _disable_lto 1

Name:		gmic
Version:	2.0.0
Release:	1
Group:		Graphics
# CeCILL version 2.0
License:	CeCILL
Summary:	A script language (G'MIC) dedicated to image processing
Url:		http://gmic.eu
Source0:	https://github.com/dtschump/gmic/archive/v.%(echo %{version} |sed -e 's,\.,,g').tar.gz
Source100:	%{name}.rpmlintrc
BuildRequires:	ffmpeg-devel
BuildRequires:  pkgconfig(Qt5Xml)
BuildRequires:	pkgconfig(fftw3)
BuildRequires:	pkgconfig(gimp-2.0)
BuildRequires:	pkgconfig(GraphicsMagick)
BuildRequires:	pkgconfig(opencv)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(libcurl)

%description
G'MIC defines a complete image processing framework, and thus 
can manage generic image data as other image-related tools. 

Anyway, the specific features described below make it a bit particular :

* It internally works with lists of images. 
  Image manipulations and interactions can be done 
  either grouped or focused on specific items.
* It can process a wide variety of image types, 
  including multi-spectral (arbitray number of channels)
  and 3d volumetric images, as well as image sequences, 
  or 3d vector objects. 
  Images with different pixel types are supported, 
  allowing to process flawlessly images with 8bits or 
  16bits integers per channel, as well as float-valued datasets.
* It provides small but efficient visualization modules 
  dedicated to the exploration/viewing of 2d/3d multi-spectral images, 
  3d vector objects (elevation map, isocurves, isosurfaces,...), 
  or 1d graph plots.
* It proposes commands to handle custom interactive windows 
  where events can be managed easily by the user.
* It is highly extensible through the importation of custom command 
  files which add new commands that become understood by the 
  language interpreter.
* Most of the functionalities can be used inside GIMP 
  via the provided plug-in, allowing end-users to integrate 
  any G'MIC-based pipeline directly in a nice GUI, 
  without coding efforts.
* It is based on the latest development versions of the CImg Library, 
  a well established C++ template image processing toolkit, 
  developed by the same team of developers.

%files
%doc COPYING README
%{_bindir}/%{name}

#------------------------------------------------------

%package -n gimp-plugin-%{name}
Summary:	gmic plugin for gimp
Group:		Graphics
Requires:	gimp >= 2.6.0
Obsoletes:	%{name}-gimp < 1.5.1.5-1
Provides:	%{name}-gimp = %{version}-%{release}
Conflicts:	%{name} < 1.5.1.5-1

%description -n gimp-plugin-%{name}
G'MIC has been made available as an easy-to-use plug-in for GIMP.
It extends this retouching software capabilities by offering a large number of
pre-defined image filters and effects.
Of course, the plug-in is highly customizable and it is possible to add your
own custom G'MIC-written filters in it.

%files -n gimp-plugin-%{name}
%{_libdir}/gimp/2.0/plug-ins/gmic_gimp_gtk
%{_libdir}/gimp/2.0/plug-ins/gmic_film_cluts.gmz

#------------------------------------------------------

%package -n %{libname}
Summary:	Library for gmic
Group:		System/Libraries
Requires:	%{name} = %{version}-%{release}
Conflicts:	%{name} < 1.5.1.5-1

%description -n %{libname}
This package contains the library needed to run programs
dynamically linked with gmic.

%files -n %{libname}
%{_libdir}/lib%{name}.so.%{major}*
%{_libdir}/lib%{name}.so.1

#------------------------------------------------------

%package -n %{develname}
Summary:	Header file for gmic
Group:		Development/C++
Requires:	%{name} = %{version}-%{release}
Obsoletes:	%{name}-gimp-devel < 1.5.1.5-1
Provides:	%{name}-devel = %{version}-%{release}
Conflicts:	%{name} < 1.5.1.5-1

%description -n %{develname}
This package contains the development file for gmic.

%files -n %{develname}
%{_includedir}/%{name}.h
%{_libdir}/lib%{name}.so

#------------------------------------------------------

%prep
%setup -qn %{name}-v.%(echo %{version} |sed -e 's,\.,,g')

%build
%setup_compile_flags
sed -i -e "s/qmake zart.pro/qmake-qt5 zart.pro/g" src/Makefile

# (tpg) use OMP form llvm
sed -i -e "s/-lgomp/-fopenmp/g" CMakeLists.txt src/Makefile

pushd src
sed -i -e 's,LIB = lib,LIB = %{_lib},' Makefile
%make
popd


%install
pushd src
%makeinstall_std
popd
