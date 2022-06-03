from uuid import UUID

from alpaca.broker import (
    BrokerClient,
    CreateJournalRequest,
    JournalEntryType,
    Journal,
    CreateBatchJournalRequest,
    BatchJournalResponse,
    CreateReverseBatchJournalRequest,
)
from alpaca.common.enums import BaseURL

from ..factories import (
    create_dummy_batch_journal_entries,
    create_dummy_reverse_batch_journal_entries,
)


def test_create_journal(reqmock, client: BrokerClient):
    reqmock.post(
        f"{BaseURL.BROKER_SANDBOX}/v1/journals",
        text="""
               {
              "id": "a7a50677-2983-4c68-96dc-aff62fe3b8cf",
              "to_account": "a4c80770-edca-45bc-b35c-cfdf2ed46649",
              "entry_type": "JNLC",
              "status": "executed",
              "from_account": "ff7b9e35-90e7-453d-a410-b508e1971a36",
              "settle_date": "2020-12-24",
              "system_date": "2020-12-24",
              "net_amount": "115.5"
             }
            """,
    )

    request = CreateJournalRequest(
        to_account="a4c80770-edca-45bc-b35c-cfdf2ed46649",
        entry_type=JournalEntryType.CASH,
        from_account="ff7b9e35-90e7-453d-a410-b508e1971a36",
        amount=115.5,
    )

    response = client.create_journal(request)

    assert reqmock.called_once
    assert isinstance(response, Journal)
    assert response.to_account == UUID("a4c80770-edca-45bc-b35c-cfdf2ed46649")


def test_batch_journal(reqmock, client: BrokerClient):
    reqmock.post(
        f"{BaseURL.BROKER_SANDBOX}/v1/journals/batch",
        text="""
        [
          {
            "error_message": "",
            "id": "0a9152c4-d232-4b00-9102-5fa19aca40cb",
            "entry_type": "JNLC",
            "from_account": "8f8c8cee-2591-4f83-be12-82c659b5e748",
            "to_account": "d7017fd9-60dd-425b-a09a-63ff59368b62",
            "symbol": "",
            "qty": null,
            "price": null,
            "status": "pending",
            "settle_date": null,
            "system_date": null,
            "net_amount": "10",
            "description": ""
          },
          {
            "error_message": "",
            "id": "84379534-bcee-4c22-abe8-a4a6286dd100",
            "entry_type": "JNLC",
            "from_account": "8f8c8cee-2591-4f83-be12-82c659b5e748",
            "to_account": "94fa473d-9a92-40cd-908c-25da9fba1e65",
            "symbol": "",
            "qty": null,
            "price": null,
            "status": "pending",
            "settle_date": null,
            "system_date": null,
            "net_amount": "100",
            "description": ""
          }
        ]
            """,
    )

    response = client.create_batch_journal(
        CreateBatchJournalRequest(
            from_account="8f8c8cee-2591-4f83-be12-82c659b5e748",
            entry_type=JournalEntryType.CASH,
            entries=create_dummy_batch_journal_entries(),
        )
    )

    assert reqmock.called_once
    assert len(response) == 2
    assert isinstance(response[0], BatchJournalResponse)


def test_reverse_batch_journal(reqmock, client: BrokerClient):
    reqmock.post(
        f"{BaseURL.BROKER_SANDBOX}/v1/journals/reverse_batch",
        text="""
            [
              {
                "error_message": "",
                "id": "0a9152c4-d232-4b00-9102-5fa19aca40cb",
                "entry_type": "JNLC",
                "from_account": "94fa473d-9a92-40cd-908c-25da9fba1e65",
                "to_account": "d7017fd9-60dd-425b-a09a-63ff59368b62",
                "symbol": "",
                "qty": null,
                "price": null,
                "status": "pending",
                "settle_date": null,
                "system_date": null,
                "net_amount": "10",
                "description": ""
              },
              {
                "error_message": "",
                "id": "84379534-bcee-4c22-abe8-a4a6286dd100",
                "entry_type": "JNLC",
                "from_account": "8f8c8cee-2591-4f83-be12-82c659b5e748",
                "to_account": "d7017fd9-60dd-425b-a09a-63ff59368b62",
                "symbol": "",
                "qty": null,
                "price": null,
                "status": "pending",
                "settle_date": null,
                "system_date": null,
                "net_amount": "100",
                "description": ""
              }
            ]
                """,
    )

    response = client.create_reverse_batch_journal(
        CreateReverseBatchJournalRequest(
            to_account="d7017fd9-60dd-425b-a09a-63ff59368b62",
            entry_type=JournalEntryType.CASH,
            entries=create_dummy_reverse_batch_journal_entries(),
        )
    )

    assert reqmock.called_once
    assert len(response) == 2
    assert isinstance(response[0], BatchJournalResponse)
