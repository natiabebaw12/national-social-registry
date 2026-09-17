import logging

from openg2p_registry_core.models import G2PRegisterChangeRequest
from openg2p_registry_core.models.enum import ChangeActionEnum
from openg2p_registry_core.services import G2PRegisterDomainService
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.attributes import flag_modified

from .utils.validations import (
    as_int,
    ensure_end_on_or_after_start,
    has_keys,
    parse_date,
    validation_error,
)

_logger = logging.getLogger("g2p-register-individualstipendprogram-service")

_SKIP_RANGE_ACTIONS = {
    ChangeActionEnum.NO_CHANGE.value,
    ChangeActionEnum.DELETE.value,
}


class G2PRegisterDomainServiceIndividualStipendProgram(G2PRegisterDomainService):
    async def validate_domain_attributes(self, records: list[dict]):
        for record in records:
            if has_keys(record, "contribution_from_date", "contribution_to_date"):
                ensure_end_on_or_after_start(
                    parse_date(record.get("contribution_from_date")),
                    parse_date(record.get("contribution_to_date")),
                    start_label="contribution_from_date",
                    end_label="contribution_to_date",
                )
            if has_keys(record, "hours_contributed"):
                hours = as_int(record.get("hours_contributed"))
                if hours is not None and hours < 0:
                    validation_error("hours_contributed must not be negative")
            if has_keys(record, "contribution_date_range"):
                date_range = as_int(record.get("contribution_date_range"))
                if date_range is not None and date_range < 0:
                    validation_error("contribution_date_range must not be negative")

    async def pre_approve(self, change_request: G2PRegisterChangeRequest, session: AsyncSession):
        from openg2p_registry_core.models import G2PRegisterChangeRequestPayload
        from ..models.individual_stipend_program import G2PRegisterIndividualStipendProgram

        payload_obj = await session.get(
            G2PRegisterChangeRequestPayload, change_request.change_request_id
        )
        if not payload_obj or not payload_obj.change_payload:
            return

        payload_changed = False
        for record in payload_obj.change_payload:
            if record.get("edit_action") in _SKIP_RANGE_ACTIONS:
                continue

            from_date = record.get("contribution_from_date")
            to_date = record.get("contribution_to_date")
            if record.get("edit_action") == ChangeActionEnum.UPDATE.value:
                existing = await session.get(
                    G2PRegisterIndividualStipendProgram,
                    record.get("internal_record_id"),
                )
                if existing:
                    if "contribution_from_date" not in record:
                        from_date = existing.contribution_from_date
                    if "contribution_to_date" not in record:
                        to_date = existing.contribution_to_date

            date_range = self._compute_contribution_date_range(from_date, to_date)
            if date_range is None:
                continue
            if record.get("contribution_date_range") != date_range:
                record["contribution_date_range"] = date_range
                payload_changed = True

        if payload_changed:
            flag_modified(payload_obj, "change_payload")
            session.add(payload_obj)

    async def post_ingest(self, register_id: str, register_row, session: AsyncSession):
        date_range = self._compute_contribution_date_range(
            getattr(register_row, "contribution_from_date", None),
            getattr(register_row, "contribution_to_date", None),
        )
        if date_range is None:
            return
        register_row.contribution_date_range = date_range
        session.add(register_row)

    @staticmethod
    def _compute_contribution_date_range(from_value, to_value) -> int | None:
        start = parse_date(from_value)
        end = parse_date(to_value)
        if start is None or end is None:
            return None
        return (end.year - start.year) * 12 + (end.month - start.month) + 1

    def construct_search_text(self, payload: dict, extra: list[str] = None) -> str:
        _logger.info("Constructing search text for individual stipend program")

        keys = ["functional_record_id", "stipend_program_name", "work_type"]
        search_text = []
        if extra:
            search_text.extend(str(value).strip() for value in extra if str(value).strip())
        search_text.extend(
            str(payload.get(key) or "").strip()
            for key in keys
            if str(payload.get(key) or "").strip()
        )

        return " ".join(search_text).strip()

    def construct_record_name(self, payload: dict, extra: list[str] = None) -> str:
        _logger.info("Constructing record name for individual stipend program")

        keys = ["stipend_program_name", "functional_record_id"]
        record_name = []
        if extra:
            record_name.extend(str(item).strip() for item in extra if str(item).strip())
        record_name.extend(
            str(payload.get(key) or "").strip()
            for key in keys
            if str(payload.get(key) or "").strip()
        )

        return " ".join(record_name).strip()
