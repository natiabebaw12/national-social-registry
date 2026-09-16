from datetime import date
from typing import Optional

from openg2p_registry_core.schemas import (
    G2PRegisterBaseSchema,
    G2PRegisterHistorySchema,
    G2PIntakeFormSchemaBase,
)
from ..models.enums import StipendProgramEnum, WorkTypeEnum


class G2PSchemaIndividualStipendProgram:
    stipend_program_name: Optional[StipendProgramEnum] = None
    work_type: Optional[WorkTypeEnum] = None
    hours_contributed: Optional[int] = None
    contribution_from_date: Optional[date] = None
    contribution_to_date: Optional[date] = None
    contribution_date_range: Optional[int] = None


class G2PRegisterSchemaIndividualStipendProgram(
    G2PRegisterBaseSchema, G2PSchemaIndividualStipendProgram
):
    """
    Schema for Project Social Contribution (stipend program) rows.
    Month/year is a from–to range; total_spent is the ministry spend on that period.
    """


class G2PIntakeFormSchemaIndividualStipendProgram(
    G2PIntakeFormSchemaBase, G2PRegisterBaseSchema, G2PSchemaIndividualStipendProgram
):
    pass


class G2PRegisterHistorySchemaIndividualStipendProgram(G2PRegisterHistorySchema):
    stipend_program_name: Optional[StipendProgramEnum] = None
    work_type: Optional[WorkTypeEnum] = None
    hours_contributed: Optional[int] = None
    contribution_from_date: Optional[date] = None
    contribution_to_date: Optional[date] = None
    total_spent: Optional[float] = None
