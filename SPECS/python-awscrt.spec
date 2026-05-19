%global desc %{expand:
Python bindings for the AWS Common Runtime}


Name:           python-awscrt
Version:        0.31.1
Release:        1%{?dist}

Summary:        Python bindings for the AWS Common Runtime
# All files are licensed under Apache-2.0, except:
# - crt/aws-c-common/include/aws/common/external/cJSON.h is MIT
# - crt/aws-c-common/source/external/cJSON.c is MIT
# - crt/s2n/pq-crypto/kyber_r3/KeccakP-brg_endian_avx2.h is BSD-3-Clause
License:        Apache-2.0 AND MIT AND BSD-3-Clause
URL:            https://github.com/awslabs/aws-crt-python

Source0:        %{pypi_source awscrt}

# two tests require internet connection, skip them
Patch0:         skip-tests-requiring-network.patch
# skip SHA1 in test_crypto
Patch1:         skip-SHA1-in-test_crypto.patch
# websockets test fail fix
Patch2:         websockets.patch
# remove FIPS version check in s2n
Patch3:         s2n-remove-fips-version-check.patch

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  openssl-devel
BuildRequires:  python%{python3_pkgversion}-websockets


%description
%{desc}


%package -n python%{python3_pkgversion}-awscrt
Summary:        %{summary}


%description -n python%{python3_pkgversion}-awscrt
%{desc}


%prep
%autosetup -p1 -n awscrt-%{version}

# relax version requirements
sed -i -e 's/"setuptools>=75\.3\.1",/"setuptools",\n  "wheel",/' pyproject.toml
# fix bdist_wheel import for setuptools 70.0.0+
sed -i -e 's/from setuptools\.command\.bdist_wheel import bdist_wheel/from wheel.bdist_wheel import bdist_wheel/' setup.py
# package builds with the name 'unknown'
sed -i '/setuptools\.setup(/a\    name="awscrt",' setup.py


%generate_buildrequires
%pyproject_buildrequires


%build
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
* Thu Apr 09 2026 Kseniia Nivnia <knivnia@redhat.com> - 0.31.1-1
- Update to 0.31.1
  Resolves: RHEL-157871

* Wed Nov 26 2025 Kseniia Nivnia <knivnia@redhat.com> - 0.27.2-2
- Add patch fixing FIPS mode crash in awscli2
  Resolves: RHEL-131280

* Fri Sep 05 2025 Kseniia Nivnia <knivnia@redhat.com> - 0.27.2-1
- Update to 0.27.2
  Resolves: RHEL-113230

* Mon Apr 29 2024 Major Hayden <major@redhat.com> - 0.20.5-3
- Removing extra pkcs11 source now that upstream switched to public domain headers

* Mon Apr 01 2024 Major Hayden <major@redhat.com> - 0.20.5-2
- Bump revision for new build

* Wed Mar 27 2024 Major Hayden <major@redhat.com> - 0.20.5-1
- Update to 0.20.5

* Tue Mar 19 2024 Major Hayden <major@redhat.com> - 0.20.2-4
- Bump revision number for new build

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
