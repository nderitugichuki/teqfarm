# Farm operations API

All paths are beneath `/api/v1/` and require JWT authentication.

## Poultry houses

- `farm/houses/` supports list, create, retrieve, update, and archive-ready status fields.
- Workers have read access. Administrators and managers can make changes.
- Responses include calculated occupancy and available capacity.

## Flocks

- `flocks/suppliers/` manages bird suppliers.
- `flocks/breeds/` manages breeds.
- `flocks/batches/` manages flock batches and creates an arrival movement automatically.
- `flocks/movements/` lists and creates mortality, sale, and adjustment movements.

Bird balances are changed only by transactional movement services. Batch history cannot be deleted; close a batch by changing its status to `closed`.

## Daily records

- `daily-records/` records eggs, feed issued, water notes, sickness, mortality, and observations.
- One record is allowed per batch and date.
- Mortality automatically creates or reconciles a bird movement and the batch balance.
- Deleting a daily record reverses its linked mortality movement.
- Workers can view and manage their own records. Managers and administrators can manage all records.

