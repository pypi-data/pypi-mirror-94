#!/usr/bin/env bash
# shellcheck disable=SC1090
# shellcheck disable=SC2034
# ${1} - project_path
# ${2} - bump: <major|minor>
# ${3} - twine: <"${GITHUB_USERNAME}"|"${NFERX_GITHUB_USERNAME}"|pypi>
# ${4} - site (default use virtual environment if no defined)
export starting="${BASH_SOURCE[0]}"; debug.sh starting

if ! isuserdarwin.sh || [[ "${USERNAME}" != "${USER}" ]]; then
  /usr/local/bin/error.sh "Can not be done with root and user should be: ${USERNAME}"; exit 1
fi

if [[ "${1-}" ]]; then
  while (( "$#" )); do
    case "${1}" in
      major) bump="${1}" ;;
      minor) bump="${1}" ;;
      patch) bump="${1}" ;;
      "${GITHUB_USERNAME}") twine="${1}" ;;
      "${NFERX_GITHUB_USERNAME}") twine="${1}" ;;
      pypi) twine="${1}" ;;
      git) twine="${1}"; git=git ;;
      site) site="${1}"; export site ;;
      bapy) name="${1}"; project_path="${BAPY}" ;;
      pen) name="${1}"; project_path="${PEN}"; twine=git; git=git ;;
      *) project_path="${PEN}"; name="$( basename "${project_path}" )" ;;
    esac; shift
  done
else
  project_path="${BAPY}"; name="$( basename "${project_path}" )"
fi

[[ "${project_path-}" ]] || { project_path="${BAPY}"; name="$( basename "${project_path}" )"; }
bump="${bump:-patch}"
twine="${twine:-${NFERX_GITHUB_USERNAME}}"
test -n "${twine}" || { /usr/local/bin/error.sh "twine repository" "empty"; exit 1; }
export USERNAME USER GITHUB_USERNAME NFERX_GITHUB_USERNAME BAPY PEN bump twine project_path name site
/usr/local/bin/debug.sh USERNAME USER GITHUB_USERNAME NFERX_GITHUB_USERNAME BAPY PEN bump twine project_path name site

cd "${project_path}" > /dev/null 2>&1 || { error.sh "${project_path}" "invalid"; exit 1; }

if isuserdarwin.sh && [[ "${USERNAME}" == "${USER}" ]]; then
    /usr/local/bin/venv.sh "${name}"
  if [[ ! "${site-}" ]]; then
    virtual="${project_path}/venv/bin/"
    source "${virtual}activate"
    export virtual; debug.sh virtual
  fi
  export VIRTUAL_ENV PYTHONHOME; debug.sh VIRTUAL_ENV PYTHONHOME
  /usr/local/bin/clean.sh "${name}" || exit 1
  find "${project_path}" -type d -name scripts -exec chmod -R +x "{}" \;
	/usr/local/bin/gadd.sh || exit 1
  /usr/local/bin/gcommit.sh || exit 1
  /usr/local/bin/gpush.sh || exit 1
	old="$( git describe --tags --abbrev=0 )"
  if error="$( "${virtual}bump2version" --allow-dirty "${bump}" 2>&1 )"; then
    /usr/local/bin/info.sh bump2version "${name}" "${bump}"
  else
    /usr/local/bin/error.sh bump2version "${name} ${bump}" "${error}"; exit 1
  fi
  /usr/local/bin/gpush.sh || exit 1
  unset project_path
  if error="$( "${virtual}python3.9" setup.py sdist 2>&1 )"; then
    /usr/local/bin/info.sh sdist "${name}"
  else
    /usr/local/bin/error.sh sdist "${name}" "${error}"; exit 1
  fi
  if error="$( "${virtual}python3.9" setup.py bdist_wheel 2>&1 )"; then
    /usr/local/bin/info.sh wheel "${name}"
  else
    /usr/local/bin/error.sh wheel "${name}" "${error}"; exit 1
  fi
  if [[ "${twine}" = 'git' ]] ; then
    /usr/local/bin/warning.sh twine "${name}" "${twine}"
  else
    if error="$( "${virtual}twine" upload -r "${twine}" dist/* 2>&1 )"; then
      /usr/local/bin/info.sh twine "${name}" "${twine}"
    else
      /usr/local/bin/error.sh twine "${name} ${twine}" "${error}"; exit 1
    fi
  fi
  /usr/local/bin/gmerge.sh || exit 1
  /usr/local/bin/clean.sh "${name}" || exit 1
  export VIRTUAL_ENV PYTHONHOME; debug.sh VIRTUAL_ENV PYTHONHOME; unset VIRTUAL_ENV PYTHONHOME
  source deactivate > /dev/null 2>&1
  deactivate > /dev/null 2>&1
  export VIRTUAL_ENV PYTHONHOME; debug.sh VIRTUAL_ENV PYTHONHOME; unset VIRTUAL_ENV PYTHONHOME
  /usr/local/bin/success.sh tag "${name}" "${old} $( git describe --tags --abbrev=0 )"
  /usr/local/bin/upgrade.sh "${name}"
else
  /usr/local/bin/error.sh "${name}" "Can not be uploaded with root and user should be: ${USERNAME}"; exit 1
fi

cd - > /dev/null || exit 1

unset starting bump twine virtual file error name project_path PYTHONPATH VIRTUAL_ENV virtual
