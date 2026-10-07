# Postman Evidence Checklist

Submit screenshots or exported responses only after redacting credential values.

- [ ] R1: GET all books, with URL and 200 status visible
- [ ] R2: GET books using `includeISBN=true` and `sortBy=author`
- [ ] R3: Basic Auth request and 200 status; token value fully hidden
- [ ] R4: POST a fictional book, with JSON body and 200 status visible
- [ ] R5: GET the newly added book by ID
- [ ] R6: DELETE the newly added book by ID
- [ ] R7: Intentional local failure showing 401 with key values hidden
- [ ] Final successful verification after correcting R7
- [ ] Offline validator output showing all checks passed

Never export or submit a live Postman environment containing secrets.
