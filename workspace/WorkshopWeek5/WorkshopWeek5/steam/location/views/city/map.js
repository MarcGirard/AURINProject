function (doc) {
  if (doc.loccityid) {
   emit(doc.name, 1);
  }
}
