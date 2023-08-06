#!/usr/bin/env bash
# ${1} - name
# shellcheck disable=SC2034
export starting="${BASH_SOURCE[0]}"; debug.sh starting

export VIRTUAL_ENV PYTHONHOME; debug.sh VIRTUAL_ENV PYTHONHOME; unset VIRTUAL_ENV PYTHONHOME
source deactivate > /dev/null 2>&1
deactivate > /dev/null 2>&1
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
  cmd="sudo /bin/python3.9"
fi
export KALI SUDO; debug.sh KALI SUDO

if [[ "${DARWIN-}" ]]; then
  cmd="/usr/local/bin/python3.9"
  prefix="--prefix $( brew --prefix )"
  unset SUDO
fi
export DARWIN prefix; debug.sh DARWIN prefix

previous="$( ${name} v )"

#if [[ "${name}" == "bapy" ]]; then
#  # shellcheck disable=SC2086
#  if ! ${cmd} -m pip -q install ${prefix} --upgrade ${url}; then
#    /usr/local/bin/error.sh install "${name}" "${previous}"; exit 1
#  fi
#  # shellcheck disable=SC2086
#  if ! ${cmd} -m pip -q install ${prefix} --upgrade ${url}; then
#    /usr/local/bin/error.sh install "${name}" "${previous} ${new}"; exit 1
#  fi
#elif [[ "${name}" == "pen" ]]; then
#  tmp="/tmp/${name}"
#  rm="sudo rm -rf ${tmp}"
#  cd /tmp || exit 1
#  ${rm}
#  if git clone -q "${url}"; then
#    cd "${name}" || exit 1
#    # shellcheck disable=SC2086
#    if ! ${cmd} setup.py -q install; then
#      /usr/local/bin/error.sh install "${name}" "${previous}"; ${rm}; exit 1
#    fi
#  else
#    /usr/local/bin/error.sh install "${name}" "${previous}"; ${rm}; exit 1
#  fi
#fi

# shellcheck disable=SC2086
if ! ${cmd} -m pip -q install ${prefix} --upgrade ${url}; then
  /usr/local/bin/error.sh install "${name}" "${previous}"; exit 1
fi
# shellcheck disable=SC2086
if ! ${cmd} -m pip -q install ${prefix} --upgrade ${url}; then
  /usr/local/bin/error.sh install "${name}" "${previous} ${new}"; exit 1
fi

new="$( ${name} v )"

if [[ "${previous}" == "${new}" ]]; then
  /usr/local/bin/warning.sh install "${name}" "${previous} ${new}"
else
  /usr/local/bin/success.sh install "${name}" "${previous} ${new}"
fi

#${rm}

unset BAPY PEN starting error command url name error project_path DARWIN prefix previous new pr opt KALI SUDO
