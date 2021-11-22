export const ledStatus = store => store.ledStatus;

export const getLedStatus = (store) => {
  const ledStatus = ledStatus(store);
  return ledStatus;
};