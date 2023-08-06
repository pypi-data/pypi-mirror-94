#!/usr/bin/env bash
# ${1} - name
# shellcheck disable=SC2034
export starting="${BASH_SOURCE[0]}"; debug.sh starting

export VIRTUAL_ENV PYTHONHOME; debug.sh VIRTUAL_ENV PYTHONHOME; unset VIRTUAL_ENV PYTHONHOME
source deactivate > /dev/null 2>&1
export VIRTUAL_ENV PYTHONHOME; debug.sh VIRTUAL_ENV PYTHONHOME; unset VIRTUAL_ENV PYTHONHOME

if [[ "${1-}" ]]; then
  while (( "$#" )); do
    case "${1}" in
      bapy) name="${1}"; url="${name}" ;;
      pen) name="${1}"; url="${PEN_GIT}" ;;
      *) name="bapy"; url="${name}" ;;
    esac; shift
  done
else
  name="bapy"; url="${name}"
fi

export BAPY PEN name url; debug.sh BAPY PEN name url

if [[ "${KALI-}" ]]; then
  unset SUDO
fi
export KALI SUDO; debug.sh KALI SUDO

if [[ "${DARWIN-}" ]]; then
  prefix="--prefix $( brew --prefix )"
fi
export DARWIN prefix; debug.sh DARWIN prefix

case "${1}" in
  i) opt="install --upgrade ${url}"; pr=install ;;
  u) opt="uninstall ${name} -y"; pr=uninstall ;;
esac

previous="$( ${name} v )"
if [[ "${name}" == "bapy" ]]; then
  # shellcheck disable=SC2086
  if ! ${SUDO} ${PYTHON39} -m pip -q install --upgrade ${url}; then
    error.sh install "${name}" "${previous} ${new}"; exit 1
  fi
  # shellcheck disable=SC2086
  if ! ${SUDO} ${PYTHON39} -m pip -q install --upgrade ${url}; then
    error.sh install "${name}" "${previous} ${new}"; exit 1
  fi
elif [[ "${name}" == "pen" ]]; then
  tmp="/tmp/${name}"
  rm="${SUDO} rm -rf ${tmp}"
  cd /tmp || exit 1
  ${rm}
  if git clone -q "${url}"; then
    cd "${name}" || exit 1
    # shellcheck disable=SC2086
    if ! ${SUDO} ${PYTHON39} setup.py -q install; then
      error.sh install "${name}" "${previous} ${new}"; ${rm}; exit 1
    fi
  else
    error.sh install "${name}" "${previous} ${new}"; ${rm}; exit 1
  fi
fi
new="$( ${name} v )"

if [[ "${previous}" == "${new}" ]]; then
  warning.sh install "${name}" "${previous} ${new}"
else
  info.sh install "${name}" "${previous} ${new}"
fi

${rm}

unset BAPY PEN starting error command url name error project_path DARWIN prefix previous new pr opt KALI SUDO
