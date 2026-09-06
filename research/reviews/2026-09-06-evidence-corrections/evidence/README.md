# Evidence receipt archives

These deterministic gzip archives preserve the unmodified HTML bytes retrieved from the Publications Office. The official source pages include multilingual navigation; compression keeps those source bytes intact while ensuring that authored project text remains English. The migration ledger records each original retrieval timestamp and the SHA-256 hash of the decompressed HTML.

The adjacent preservation proof is authored JSON. Its ledger hash is calculated after universal-newline conversion to LF so the check remains stable across Git checkouts with different native line endings.
