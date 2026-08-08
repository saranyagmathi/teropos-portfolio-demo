\# Selected Code Examples



These files are sanitised examples selected from the private TeroPOS production codebase. They demonstrate coding style, validation, defensive programming and configuration handling without exposing commercial business logic or production configuration.



\## Backend Example



\### `backend/image\_utils.py`



Demonstrates:



\- File-extension and MIME-type validation

\- Upload-size enforcement

\- Image-content verification

\- EXIF orientation handling

\- Image resizing and WebP optimisation

\- Collision-resistant filename generation

\- Structured HTTP error responses



Internal storage-path helpers and production configuration are intentionally excluded.



\## Frontend Examples



\### `frontend/orderDateTime.ts`



Demonstrates:



\- Safe interpretation of timestamps

\- Timezone handling

\- Locale-aware date and time formatting

\- Small, reusable TypeScript utility functions



\### `frontend/appUrl.ts`



Demonstrates:



\- Environment-variable configuration

\- Development-environment fallback behaviour

\- Separation of development and production routing



The production TeroPOS domain has been replaced with `example.com`.



\## Excluded Code



This portfolio does not include authentication internals, vendor-isolation enforcement, checkout and payment processing, inventory rules, tax calculations, offline-sale synchronisation, database schemas or production deployment configuration.

