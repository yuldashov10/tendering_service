| №  | Название группы  | Ручки                                                                         | Статус | Методы                                   |
|----|:----------------:|-------------------------------------------------------------------------------|:------:|------------------------------------------|
| 01 |      /ping       | - `/ping`                                                                     |   ✅    | - `get`                                  |
| 02 |   /tenders/new   | - `/tenders/new`                                                              |   ✅    | - `create_tender`                        |
| 03 |  /tenders/list   | - `/tenders`<br/>- `/tenders/my`<br/>- `/tenders/my?username=userName`        |   ✅    | - `list`<br/>- `my_tenders`              |
| 04 | /tenders/status  | - `/tenders/status`                                                           |   ✅    | - `change_status`                        |
| 05 | /tenders/version | - `/tenders/edit`<br/>- `/tenders/rollback`                                   |   ✅    | - `update_tender`<br/>- `rollback`       |
| 06 |    /bids/new     | - `/bids/new`<br/>                                                            |   ✅    | - `create_bid`                           |
| 07 |  /bids/decision  | - `/bids/submit_decision`                                                     |   ✅    | - `submit_decision`                      |
| 08 |    /bids/list    | - `/bids/{tenderId}/list`<br/>- `/bids/my`<br/>- `/bids/my?username=userName` |   ✅    | - `list_bids_for_tender`<br/>- `my_bids` |
| 09 |   /bids/status   | - `/bids/status`                                                              |   ✅    | - `change_status`                        |
| 10 |  /bids/version   | - `/bids/edit`<br/>- `/bids/rollback`                                         |   ✅    | - `update_bid`<br/>- `rollback`          |
