# Security and Production Safety

CutBridge must not upload or transmit client assets, production files, or metadata unless a future feature explicitly requires it and the user opts in.

Update checks should exchange only the minimum data required for compatibility and release discovery. Forced updates are not appropriate for active production environments.

Never commit credentials, API tokens, private client data, NDA material, or proprietary production assets to this repository.
