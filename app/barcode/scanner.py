from fastapi import HTTPException
class BarcodeScanner:
    def __init__(self, db): self.db=db
    def lookup(self, barcode):
        with self.db.connection() as c: row=c.execute("SELECT * FROM products WHERE barcode=?",(barcode,)).fetchone()
        if not row: raise HTTPException(404,"Barcode not found")
        return dict(row)
