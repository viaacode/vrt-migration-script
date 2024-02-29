# VRT Migration Script

Script to migrate VRT v1/dailies items to their v2/S3 structure.

For every `fragment_id`:
- delete all fragemnts,
- delete all collaterals,
- add S3-metadata,
- send `essenceArchivedEvent`.
