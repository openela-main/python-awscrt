%global desc %{expand:
Python bindings for the AWS Common Runtime}


Name:           python-awscrt
Version:        0.20.2
Release:        3%{dist}

Summary:        Python bindings for the AWS Common Runtime
# All files are licensed under Apache-2.0, except:
# - crt/aws-c-common/include/aws/common/external/cJSON.h is MIT
# - crt/aws-c-common/source/external/cJSON.c is MIT
# - crt/s2n/pq-crypto/kyber_r3/KeccakP-brg_endian_avx2.h is BSD-3-Clause
License:        Apache-2.0 AND MIT AND BSD-3-Clause
URL:            https://github.com/awslabs/aws-crt-python

Source0:        %{pypi_source awscrt}

# Get an open source version of the pkcs11 header file from Simo's repository.
# https://github.com/latchset/pkcs11-headers
Source1:        https://raw.githubusercontent.com/latchset/pkcs11-headers/main/public-domain/2.40/pkcs11.h

# one test requires internet connection, skip it
Patch0:         skip-test-requiring-network.patch

BuildRequires:  python%{python3_pkgversion}-devel

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  openssl-devel

BuildRequires:  python%{python3_pkgversion}-websockets

# https://bugzilla.redhat.com/show_bug.cgi?id=2180988
ExcludeArch:    s390x


%description
%{desc}


%package -n python%{python3_pkgversion}-awscrt
Summary:        %{summary}


%description -n python%{python3_pkgversion}-awscrt
%{desc}


%prep
%autosetup -p1 -n awscrt-%{version}

# Bring in the pkcs11 header file from Simo's repository.
rm -fv crt/aws-c-io/source/pkcs11/v2.40/*
cp %{SOURCE1} crt/aws-c-io/source/pkcs11/v2.40/

# Remove the third party license that goes along with
# the removed pkcs11.h header file.
rm -rf crt/aws-c-io/THIRD-PARTY-LICENSES.txt


%generate_buildrequires
%pyproject_buildrequires


%build
%ifarch %{ix86}
# disable SSE2 instructions to prevent a crash in aws-c-common thread handling
# probably caused by a compiler bug
export CFLAGS="%{optflags} -mno-sse2"
%endif
export AWS_CRT_BUILD_USE_SYSTEM_LIBCRYPTO=1
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files _awscrt awscrt


%check
PYTHONPATH="%{buildroot}%{python3_sitearch}:%{buildroot}%{python3_sitelib}" %{python3} -m unittest


%files -n python%{python3_pkgversion}-awscrt -f %{pyproject_files}
%doc README.md


%changelog
* Tue Feb 13 2024 Major Hayden <major@redhat.com> - 0.20.2-3
- Remove the third party license file from excluded pkcs11.h

* Mon Feb 12 2024 Major Hayden <major@redhat.com> - 0.20.2-2
- Replacing upstream's pkcs11.h with Simo's public domain version.

* Tue Jan 02 2024 Packit <hello@packit.dev> - 0.20.2-1
- [packit] 0.20.2 upstream release
- Resolves rhbz#2254450

* Wed Dec 06 2023 Nikola Forró <nforro@redhat.com> - 0.19.19-2
- Add Packit config

* Thu Nov 30 2023 Packit <hello@packit.dev> - 0.19.19-1
- [packit] 0.19.19 upstream release
- Resolves rhbz#2250726

* Fri Nov 17 2023 Packit <hello@packit.dev> - 0.19.13-1
- [packit] 0.19.13 upstream release
- Resolves rhbz#2247105

* Wed Oct 25 2023 Packit <hello@packit.dev> - 0.19.6-1
- [packit] 0.19.6 upstream release
- Resolves rhbz#2211521 Upstream tag: v0.19.6 Upstream commit: b83949d0

* Mon Oct 16 2023 Packit <hello@packit.dev> - 0.19.3-1
- [packit] 0.19.3 upstream release

* Mon Oct 02 2023 Packit <hello@packit.dev> - 0.19.2-1
- [packit] 0.19.2 upstream release

* Fri Aug 25 2023 Nikola Forró <nforro@redhat.com> - 0.18.0-1
- Initial import for EPEL 9
