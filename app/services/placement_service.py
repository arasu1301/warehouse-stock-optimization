from fastapi import HTTPException
class PlacementService:
    def __init__(self, db): self.db=db
    def move(self, sku, batch_code, location):
        with self.db.connection() as c:
            cur=c.execute("UPDATE batches SET location=? WHERE sku=? AND batch_code=?",(location,sku,batch_code))
            if not cur.rowcount: raise HTTPException(404,"Batch not found")
        return {"status":"placed","location":location}
