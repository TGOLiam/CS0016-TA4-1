# AI and API Validation Log

Student: Liam Brent  Section: tn35  Date: 2026-10-07

Approved AI tool: ChatGPT

Do not paste a username, password, bearer token, API key, Authorization header,
X-API-KEY value, or private response data into this file or an AI tool.

| Request | Pre-AI prediction | Sanitized AI prompt | AI recommendation | Decision (Accepted/Modified/Rejected) | Simulator/Postman evidence |
|---|---|---|---|---|---|
| R1 | GET /api/v1/books, no authentication, 200 | Check the local API design for listing all books. No credentials or private data included. | Use GET /api/v1/books; expect 200. | Accepted | Capture Postman URL, 200 status, and response list. |
| R2 | GET /api/v1/books with includeISBN=true and sortBy=author, 200 | Check the local API query-parameter design. No credentials included. | Use the documented query parameters exactly; expect 200. | Accepted | Capture URL/Params, 200 status, ISBN fields, and sorted response. |
| R3 | POST /api/v1/loginViaBasic with Basic Auth, 200 | Check the local basic-auth login design. Do not provide credentials or token values. | Use POST with Basic Auth; expect 200. | Accepted | Capture 200 status and fully redact credentials and token. |
| R4 | POST /api/v1/books with X-API-KEY, JSON body, 200 | Check a protected local add-book request using fictional fields only. | Use POST, Content-Type application/json, X-API-KEY, and id/title/author; expect 200. | Accepted | Capture JSON body and 200 status; hide API-key value. |
| R5 | GET /api/v1/books/{id}, no authentication, 200 | Check the local request to retrieve a newly created fictional book. | Substitute the actual fictional book ID in Postman; expect 200. | Accepted | Capture URL with actual ID, 200 status, and returned book. |
| R6 | DELETE /api/v1/books/{id} with X-API-KEY, 200 | Check the local protected delete request. | Use DELETE with the actual book ID and X-API-KEY; expect 200. | Accepted | Capture URL and 200 status; hide API-key value. |
| R7 | POST /api/v1/books without valid key, 401; restore key, 200 | Check troubleshooting design for a missing or invalid key. No key values included. | Missing/invalid X-API-KEY should give 401; restore valid local key and retry. | Accepted | Capture redacted 401 failure, then repaired 200 success. |

## Python script review

- Sanitized excerpt reviewed (credential values replaced with placeholders): Yes. Any host, username, password, token, and API-key values must be replaced with placeholders before review.
- What the script automates: It uses Python HTTP requests in a loop to generate and submit many fictional book records to the library API. The JSON payload holds each book record, and Faker can generate varied fictional values. Authentication authorizes protected API operations.
- AI recommendation evaluated: Add a request timeout and verify each HTTP response status before treating a bulk-add iteration as successful.
- Decision and technical reason: Accepted. A timeout prevents indefinite waiting, while status checking identifies failed or rejected requests so they are not silently counted as successful.
- Independent validation performed: Compared the request method, endpoint, authentication design, payload fields, and expected statuses with the local OpenAPI documentation and VM/Postman execution.

## AI-use disclosure

- Assistance received: AI was used to draft sanitized request designs, evidence wording, a Python workflow explanation, and a validation checklist. No credentials, tokens, headers containing secret values, or private response data were shared.
- Checks performed before accepting suggestions: Compared every suggestion with the local OpenAPI documentation, the API Simulator, Postman responses, and the offline validator.
- Revisions made by the student: Kept the documented methods, paths, authentication labels, query parameters, JSON fields, and status codes; used fictional records only.
- One limitation or error found in the AI response: AI cannot verify the VM-only simulator or confirm a request actually succeeded; Postman/API Simulator evidence is required before final submission.

## Reflection questions

1. **Which AI recommendation did you modify or reject, and what justified the decision?**

   I did not accept any suggestion as proof by itself. The request design was accepted only after comparison with the local OpenAPI documentation and Postman results. In particular, the missing-key test was validated by the documented and observed 401 response, followed by a successful request after restoring the valid local key.

2. **How do method, path, headers, parameters, payload, and status code work together in a REST request?**

   The method defines the action, such as GET, POST, or DELETE. The path identifies the collection or individual resource. Parameters refine a request, headers describe content and supply required authentication, and a payload carries data for a POST request. The status code reports the outcome, such as 200 for a successful request or 401 when required authentication is missing or invalid.

3. **Why should credentials and tokens remain outside AI prompts and submitted evidence?**

   Credentials and tokens grant access. Sharing them in prompts, screenshots, exports, or submitted files could expose the lab environment and allow unauthorized use. They should remain only in the authorized VM and Postman configuration, with values redacted from evidence.

4. **How would rate limits, asynchronous processing, or webhooks affect a larger bulk-book workflow?**

   A bulk workflow should pace requests and retry safely when rate limits apply. For a long-running import, an asynchronous job can prevent the client from waiting for every record. A webhook can notify the automation when the job completes or fails, allowing the client to process the result without constant polling.
