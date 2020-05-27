function (doc) {
  if (doc.locstatecode && doc.total_playtime) {
   emit([doc.locstatecode, doc.name, doc.coordinates], doc.total_playtime);
  }
}
