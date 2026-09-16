import logging

from openg2p_registry_core.services import G2PRegisterDomainService

from .utils.validations import (
    as_float,
    as_int,
    ensure_end_on_or_after_start,
    has_keys,
    parse_date,
    validation_error,
)

_logger = logging.getLogger("g2p-register-individualstipendprogram-service")


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
                spent = as_int(record.get("contribution_date_range"))
                if date_range is not None and date_range < 0:
                    validation_error("contribution_date_range must not be negative")

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
