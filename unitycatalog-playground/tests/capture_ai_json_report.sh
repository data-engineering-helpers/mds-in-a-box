#!/usr/bin/env bash

set -u

: "${USE_DOCKER:=1}"
: "${EFFECTIVE_UC_SOURCE:=docker}"
: "${UC_LOCAL_ROOT:=}"
: "${AWS_ENDPOINT_URL:=http://localhost:8333}"
: "${UC_CMD:=uc}"

ts="$(date -u +"%Y%m%dT%H%M%SZ")"
out_file="tests/mds-test-${ts}.json"
cmds_tmp="$(mktemp)"
echo '{}' > "${cmds_tmp}"

run_capture() {
  local name="$1"
  local cmd="$2"
  local stdout_tmp stderr_tmp exit_code entry payload stdout_txt stderr_txt next_tmp

  stdout_tmp="$(mktemp)"
  stderr_tmp="$(mktemp)"

  eval "${cmd}" >"${stdout_tmp}" 2>"${stderr_tmp}"
  exit_code=$?

  if [[ ${exit_code} -eq 0 ]] && jq -e . "${stdout_tmp}" >/dev/null 2>&1; then
    payload="$(cat "${stdout_tmp}")"
    entry="$(jq -n --arg cmd "${cmd}" --argjson exit "${exit_code}" --argjson data "${payload}" '{ok:true, exit:$exit, cmd:$cmd, data:$data}')"
  else
    stdout_txt="$(cat "${stdout_tmp}")"
    stderr_txt="$(cat "${stderr_tmp}")"
    entry="$(jq -n --arg cmd "${cmd}" --argjson exit "${exit_code}" --arg stdout "${stdout_txt}" --arg stderr "${stderr_txt}" '{ok:($exit==0), exit:$exit, cmd:$cmd, stdout:$stdout, stderr:$stderr}')"
  fi

  next_tmp="$(mktemp)"
  jq --arg k "${name}" --argjson v "${entry}" '. + {($k): $v}' "${cmds_tmp}" > "${next_tmp}" && mv "${next_tmp}" "${cmds_tmp}"

  rm -f "${stdout_tmp}" "${stderr_tmp}"
}

host_name="$(hostname 2>/dev/null || echo unknown)"
os_type="$(uname -s 2>/dev/null || echo unknown)"
arch_type="$(uname -m 2>/dev/null || echo unknown)"

if [[ "${USE_DOCKER}" == "1" ]]; then
  effective_uc_source="docker"
else
  effective_uc_source="${EFFECTIVE_UC_SOURCE}"
fi

uc_version="$(eval "${UC_CMD} --version" 2>/dev/null | head -n 1)"
if [[ -z "${uc_version}" ]]; then
  uc_version="$(eval "${UC_CMD} -v" 2>/dev/null | head -n 1)"
fi
if [[ -z "${uc_version}" ]]; then
  uc_version="unknown"
fi

if [[ "${USE_DOCKER}" == "1" ]]; then
  seaweedfs_version="$(docker exec s3 weed version 2>/dev/null | head -n 1)"
else
  seaweedfs_version="$( (seaweedfs version 2>/dev/null || weed version 2>/dev/null) | head -n 1 )"
fi
if [[ -z "${seaweedfs_version}" ]]; then
  seaweedfs_version="unknown"
fi

run_capture "aws_s3api_list_buckets" "aws --endpoint-url ${AWS_ENDPOINT_URL} s3api list-buckets --output json"
run_capture "aws_s3api_list_objects_lakehouse" "aws --endpoint-url ${AWS_ENDPOINT_URL} s3api list-objects-v2 --bucket lakehouse --output json"
run_capture "uc_catalog_list" "${UC_CMD} catalog list --output json"
run_capture "uc_schema_list_unitysw" "${UC_CMD} schema list --catalog unitysw --output json"
run_capture "uc_table_list_unitysw_bronze" "${UC_CMD} table list --catalog unitysw --schema bronze --output json"
run_capture "uc_table_get_dim_customer" "${UC_CMD} table get --full_name unitysw.bronze.dim_customer --output json"
run_capture "uc_table_read_dim_customer" "${UC_CMD} table read --full_name unitysw.bronze.dim_customer --max_results 3 --output json"

commands_payload="$(cat "${cmds_tmp}")"

jq -n \
  --arg timestamp_utc "${ts}" \
  --arg host "${host_name}" \
  --arg os "${os_type}" \
  --arg arch "${arch_type}" \
  --arg use_docker "${USE_DOCKER}" \
  --arg uc_source "${effective_uc_source}" \
  --arg uc_local_root "${UC_LOCAL_ROOT}" \
  --arg aws_endpoint "${AWS_ENDPOINT_URL}" \
  --arg uc_version "${uc_version}" \
  --arg seaweedfs_version "${seaweedfs_version}" \
  --argjson commands "${commands_payload}" \
  '{
    metadata: {
      timestamp_utc: $timestamp_utc,
      host: $host,
      os: $os,
      architecture: $arch,
      use_docker: $use_docker,
      effective_uc_source: $uc_source,
      uc_local_root: $uc_local_root,
      aws_endpoint: $aws_endpoint,
      uc_version: $uc_version,
      seaweedfs_version: $seaweedfs_version
    },
    commands: $commands
  }' > "${out_file}"

rm -f "${cmds_tmp}"

echo "Wrote AI report to ${out_file}"
