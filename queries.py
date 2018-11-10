get_accredited_crl_info_query = '''SELECT
  aci.sha1Hash,
  aci.crlUrl
FROM accredited_cert_info aci
WHERE aci.active = 1
AND aci.archive = 0
;'''


get_crl_hash_query = '''SELECT acii.crlSha1Hash as crl_db_hash,
acii.crlLocation as crl_location
  FROM accredited_crl_installed_info acii
WHERE acii.server = %(server)s
AND acii.certificateSha1Hash = '%(sha1Hash)s'
;'''


insert_crl_hash_query = '''INSERT INTO accredited_crl_installed_info (server, certificateSha1Hash, crlSha1Hash, createDateTime)
  VALUES (%(server)s, '%(sha1Hash)s', NULL, NOW());'''


update_crl_hash_query = '''UPDATE accredited_crl_installed_info acii
SET acii.crlSha1Hash = '%(crl_file_hash)s',
acii.crlLocation = '%(crl_actual_file)s',
acii.updateDateTime = NOW()
WHERE acii.server = %(server)s
AND acii.certificateSha1Hash = '%(sha1Hash)s'
AND acii.archive = 0
;'''
