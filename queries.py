get_accredited_crl_info_query = '''SELECT
  aci.sha1Hash,
  aci.crlUrl
FROM accredited_cert_info aci
WHERE aci.fileVersion = (SELECT
    MAX(aci.fileVersion)
  FROM accredited_cert_info
  WHERE aci.active = 1
  AND aci.archive = 0)
AND aci.active = 1
AND aci.archive = 0
;'''


get_crl_hash_query = '''SELECT acii.crlSha1Hash as crl_db_hash,
acii.crlLocation as crl_location
  FROM accredited_crl_installed_info acii
WHERE acii.server = %(server)s
AND acii.certificateSha1Hash = '%(sha1Hash)s'
;'''


insert_crl_hash_query = '''INSERT INTO accredited_crl_installed_info (server, certificateSha1Hash, crlSha1Hash, createDateTime, lastStatus)
  VALUES (%(server)s, '%(sha1Hash)s', NULL, NOW(), 'AWAITING');'''


update_crl_hash_query_ok = '''UPDATE accredited_crl_installed_info acii
SET acii.crlSha1Hash = '%(crl_file_hash)s',
acii.crlLocation = '%(crl_actual_file)s',
acii.updateDateTime = NOW(),
acii.lastStatus = 'INSTALLED'
WHERE acii.server = %(server)s
AND acii.certificateSha1Hash = '%(sha1Hash)s'
AND acii.archive = 0
;'''


update_crl_hash_query_bad = '''UPDATE accredited_crl_installed_info acii
SET acii.crlSha1Hash = '%(crl_file_hash)s',
acii.crlLocation = '%(crl_bad_file)s',
acii.updateDateTime = NOW(),
acii.lastStatus = 'NOT_INSTALLED'
WHERE acii.server = %(server)s
AND acii.certificateSha1Hash = '%(sha1Hash)s'
AND acii.archive = 0
;'''


update_set_download_fail_query = '''UPDATE accredited_crl_installed_info acii
SET acii.lastStatus = 'DOWNLOAD_FAILED'
WHERE acii.server = %(server)s
AND acii.certificateSha1Hash = '%(sha1Hash)s'
AND acii.archive = 0
;'''