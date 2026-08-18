# Applications

`apps/` contains deployable composition roots only. Applications may call public module interfaces and compose approved dependencies; they must not own cross-platform domain policy or access another module's storage directly.

The first application behavior begins in B1, tenant-aware identity and protected API entry. The directories created during B0 are placeholders for approved deployment boundaries, not running services.

