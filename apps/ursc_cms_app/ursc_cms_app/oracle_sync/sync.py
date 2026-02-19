import frappe
import oracledb

def sync_to_oracle(doc, method=None):
    """Sync Purchase Receipt data directly into Oracle DB."""
    dsn = oracledb.makedsn("localhost", 1521, service_name="XEPDB1")
    data = {
        "pr_id": doc.name,
        "supplier_name": doc.supplier,
        "posting_date": str(doc.posting_date),
        "total_amount": float(doc.total or 0),
        "status": doc.status,
        "remarks": doc.remarks or ""
    }

    try:
        with oracledb.connect(user="sample_oracle_db", password="N33mu$123", dsn=dsn) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    MERGE INTO purchase_receipts t
                    USING (SELECT :pr_id AS pr_id FROM dual) s
                    ON (t.pr_id = s.pr_id)
                    WHEN MATCHED THEN
                        UPDATE SET supplier_name=:supplier_name,
                                   posting_date=TO_DATE(:posting_date,'YYYY-MM-DD'),
                                   total_amount=:total_amount,
                                   status=:status,
                                   remarks=:remarks,
                                   updated_at=SYSDATE
                    WHEN NOT MATCHED THEN
                        INSERT (pr_id, supplier_name, posting_date, total_amount, status, remarks)
                        VALUES (:pr_id, :supplier_name, TO_DATE(:posting_date,'YYYY-MM-DD'),
                                :total_amount, :status, :remarks)
                """, data)
                conn.commit()
        frappe.logger().info(f"✅ Oracle sync success for {doc.name}")
    except Exception as e:
        frappe.log_error(f"Oracle sync failed: {e}", "Oracle Sync Error")

