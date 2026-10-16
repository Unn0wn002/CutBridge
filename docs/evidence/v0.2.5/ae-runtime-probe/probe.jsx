var cbFile = new File("C:/Evidence/ae-host.txt");
cbFile.open("w"); cbFile.write("version=" + app.version + "\n"); cbFile.close();
app.quit();
