(function () {
  app.newProject();
  var c = app.project.items.addComp("diagC", 100, 100, 1, 1, 24), f = app.project.items.addFolder("diagF");
  var out = [];
  for (var i = 1; i <= app.project.numItems; i++) { var it = app.project.item(i); out.push(it.name + " typeName=" + it.typeName + " isComp=" + (it instanceof CompItem) + " isFolder=" + (it instanceof FolderItem) + " numLayers=" + it.numLayers); }
  var r = new File(new File($.fileName).parent.fsName + "/diag-typename.txt"); r.encoding = "UTF-8"; r.open("w"); r.write(out.join("\n")); r.close();
  app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);
}());
