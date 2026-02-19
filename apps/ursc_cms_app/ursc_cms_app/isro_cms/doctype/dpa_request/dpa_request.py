import frappe

from frappe.model.document import Document
 
class DPARequest(Document):
 
    def after_workflow_action(self, action):

        """

        Runs ONLY when workflow action is executed

        """
 
        user = frappe.session.user

        now = frappe.utils.now_datetime()
 
        # ==========================

        # APPROVE ACTION

        # ==========================

        if action == "Approve":

            self.db_set({

                "dpa_status_flag": 1,

                "approved_by": user,

                "approved_on": now,

                "rejected_by": None,

                "rejected_on": None

            }, update_modified=False)
 
        # ==========================

        # REJECT ACTION

        # ==========================

        elif action == "Reject":

            self.db_set({

                "dpa_status_flag": 2,

                "rejected_by": user,

                "rejected_on": now,

                "approved_by": None,

                "approved_on": None

            }, update_modified=False)
 
        # ==========================

        # SEND BACK / RESET

        # ==========================

        elif action in ("Send Back", "Reset", "Set Pending"):

            self.db_set({

                "dpa_status_flag": 0,

                "approved_by": None,

                "approved_on": None,

                "rejected_by": None,

                "rejected_on": None

            }, update_modified=False)

 