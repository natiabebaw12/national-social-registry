from datetime import date

from sqlalchemy import Date, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from openg2p_registry_core.models import G2PRegister, G2PRegisterHistory
from openg2p_registry_core.models.g2p_intake_form import G2PIntakeForm

from ..services import G2PRegisterDomainServiceIndividualStipendProgram
from .enums import StipendProgramEnum, WorkTypeEnum


class G2PIndividualStipendProgram:
    stipend_program_name: Mapped[StipendProgramEnum] = mapped_column(String, nullable=True)
    work_type: Mapped[WorkTypeEnum] = mapped_column(String, nullable=True)
    hours_contributed: Mapped[int] = mapped_column(Integer, nullable=True)
    contribution_from_date: Mapped[date] = mapped_column(Date, nullable=True)
    contribution_to_date: Mapped[date] = mapped_column(Date, nullable=True)
    contribution_date_range: Mapped[int] = mapped_column(Integer, nullable=True)


class G2PRegisterIndividualStipendProgram(G2PRegister, G2PIndividualStipendProgram):
    __tablename__ = "g2p_register_individual_stipend_programs"

    def get_record_name_fields(self) -> str:
        """Return stipend program fields used to build record_name."""
        return G2PRegisterDomainServiceIndividualStipendProgram().construct_record_name(self.to_dict())

    def get_search_text_fields(self) -> str:
        """Return stipend program fields used to build search_text."""
        return G2PRegisterDomainServiceIndividualStipendProgram().construct_search_text(self.to_dict())


class G2PIntakeFormIndividualStipendProgram(G2PIntakeForm, G2PRegister, G2PIndividualStipendProgram):
    __tablename__ = "g2p_intake_form_individual_stipend_programs"

    def get_record_name_fields(self) -> str:
        """Return stipend program fields used to build record_name."""
        return G2PRegisterDomainServiceIndividualStipendProgram().construct_intake_record_name(self.to_dict())

    def get_search_text_fields(self) -> str:
        """Return stipend program fields used to build search_text."""
        return G2PRegisterDomainServiceIndividualStipendProgram().construct_search_text(self.to_dict())


class G2PRegisterHistoryIndividualStipendProgram(G2PRegisterHistory, G2PIndividualStipendProgram):
    __tablename__ = "g2p_register_history_individual_stipend_programs"
