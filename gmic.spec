%define major 2
%define libname %mklibname %{name} %{major}
%define develname %mklibname -d %{name}

%define cmajor 2
%define clibname %mklibname cgmic %{cmajor}
%define cdevelname %mklibname -d cgmic

%define _disable_lto 1
%ifarch aarch64
%global optflags %{optflags} -fuse-ld=bfd
%endif

Name:		gmic
Version:	2.5.7
Release:	1
Group:		Graphics
# CeCILL version 2.0
License:	CeCILL
Summary:	A script language (G'MIC) dedicated to image processing
Url:		http://gmic.eu
Source0:	https://github.com/dtschump/gmic/archive/gmic-v.%{version}.tar.gz
Source1:	https://github.com/c-koi/gmic-qt/archive/gmic-qt-v.2.5.6.tar.gz
Source2:	https://github.com/c-koi/zart/archive/zart-master.tar.gz
Source3:	https://github.com/dtschump/gmic-community/archive/gmic-community-master.tar.gz
Source4:	https://github.com/dtschump/CImg/archive/CImg-v.%{version}.tar.gz
Source5:	http://gmic.eu/gmic_stdlib.h
Source100:	%{name}.rpmlintrc
BuildRequires:	ffmpeg-devel
BuildRequires:	qmake5
BuildRequires:	pkgconfig(OpenEXR)
BuildRequires:	pkgconfig(libtiff-4)
BuildRequires:	pkgconfig(libjpeg)
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5Gui)
BuildRequires:	pkgconfig(Qt5Network)
BuildRequires:	pkgconfig(Qt5Widgets)
BuildRequires:	pkgconfig(Qt5Xml)
BuildRequires:	pkgconfig(fftw3)
BuildRequires:	pkgconfig(gimp-2.0)
BuildRequires:	pkgconfig(GraphicsMagick)
BuildRequires:	pkgconfig(opencv)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(x11)
BuildRequires:	libatomic-devel
# gmic Makefiles are rather broken and will prefer
# /usr/include/gmic.h over the local gmic.h
BuildConflicts: gmic-devel

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
%{_libdir}/gimp/2.0/plug-ins/gmic_gimp_qt
%{_libdir}/gimp/2.0/plug-ins/gmic_cluts.gmz

#------------------------------------------------------

%package -n krita-plugin-%{name}
Summary:	gmic plugin for Krita
Group:		Graphics
Requires:	krita >= 3.0

%description -n krita-plugin-%{name}
G'MIC has been made available as an easy-to-use plug-in for Krita.
It extends this retouching software capabilities by offering a large number of
pre-defined image filters and effects.
Of course, the plug-in is highly customizable and it is possible to add your
own custom G'MIC-written filters in it.

%files -n krita-plugin-%{name}
%{_bindir}/gmic_krita_qt

#------------------------------------------------------

%package qt
Summary:	Qt frontend for applying g'mic filters
Group:		Graphics

%description qt
Qt frontend for applying g'mic filters

%files qt
%{_bindir}/gmic_qt

#------------------------------------------------------

%package zart
Summary:	Application for applying live effects to Webcam images
Group:		Graphics

%description zart
Application for applying live effects to Webcam images

%files zart
%{_bindir}/zart

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

%package -n %{clibname}
Summary:	C Library for gmic
Group:		System/Libraries
Requires:	%{libname} = %{EVRD}

%description -n %{clibname}
This package contains the library needed to run programs
dynamically linked with gmic's C bindings

%files -n %{clibname}
%{_libdir}/libc%{name}.so.%{cmajor}*

#------------------------------------------------------

%package -n %{cdevelname}
Summary:	Header file for gmic C bindings
Group:		Development/C
Requires:	%{develname} = %{EVRD}

%description -n %{cdevelname}
This package contains the development file for gmic C bindings.

%files -n %{cdevelname}
%{_includedir}/%{name}_libc.h
%{_libdir}/libc%{name}.so

#------------------------------------------------------

%prep
%setup -qn %{name}-v.%{version} -a 1 -a 2 -a 3 -a 4
pushd ..
rm -rf gmic-qt* zart* gmic-community* CImg*
popd
mv gmic-qt-v.* ../gmic-qt
mv zart-* zart
mv gmic-community-* ../gmic-community
mv CImg-* ../CImg
ln -s ../gmic-qt ../gmic-community ../CImg .

#cd ../gmic-qt/src
#ln -s ../../CImg/CImg.h .

%build
%setup_compile_flags

# (tpg) use OMP form llvm
sed -i -e "s/-lgomp/-fopenmp/g" src/Makefile

cd src
# Fix install location...
sed -i -e 's,LIB = lib,LIB = %{_lib},' Makefile
# And pass compiler flags while linking (vital for -flto)
sed -i -e 's|-Wl,-soname|$(CFLAGS) -Wl,-soname|' Makefile
%make clean
cp %{SOURCE5} .
# We can save some compile time by generating a PCH for CImg...
%make WGET=false CC=%{__cc} CXX=%{__cxx} check_versions gmic.cpp gmic.h gmic_stdlib.h CImg.h
#%{__cxx} %{optflags} -x c++-header -std=c++11 -fopenmp -c CImg.h -o CImg.h.pch
#%{__cxx} %{optflags} -x c++-header -std=c++11 -fopenmp -c gmic.h -o gmic.h.pch
#-include-pch CImg.h.pch -include-pch gmic.h.pch
%make WGET=false CC=%{__cc} CXX=%{__cxx} OPT_CFLAGS="%{optflags}" NOSTRIP=1 lib
%make WGET=false CC=%{__cc} CXX=%{__cxx} OPT_CFLAGS="%{optflags}" NOSTRIP=1 libc
%make WGET=false CC=%{__cc} CXX=%{__cxx} OPT_CFLAGS="%{optflags}" NOSTRIP=1 cli
%make WGET=false QMAKE=qmake-qt5 CC=%{__cc} CXX=%{__cxx} OPT_CFLAGS="%{optflags}" zart
%make WGET=false QMAKE=qmake-qt5 CC=%{__cc} CXX=%{__cxx} OPT_CFLAGS="%{optflags}" QT_GMIC_PATH="$(pwd)" gmic_qt
%make WGET=false QMAKE=qmake-qt5 CC=%{__cc} CXX=%{__cxx} OPT_CFLAGS="%{optflags}" QT_GMIC_PATH="$(pwd)" krita
%make WGET=false QMAKE=qmake-qt5 CC=%{__cc} CXX=%{__cxx} OPT_CFLAGS="%{optflags}" QT_GMIC_PATH="$(pwd)" gimp

%install
cd src
%makeinstall_std
cd -
