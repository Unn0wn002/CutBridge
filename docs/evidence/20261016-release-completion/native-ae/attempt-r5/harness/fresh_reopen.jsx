$.evalFile(new File('C:/NativeAEInput/reopen.jsx'));
CB.save(CB.config.output_root+'/fresh-process-reopen.json',{status:CB.report.status,candidate_sha:CB.report.candidate_sha,host_version:app.version,checks:CB.report.checks,error:CB.report.error,process_restart:'Launcher must prove distinct PID, prior exit and current exit',normal_quit_requested:true});
try{if(app.project)app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);}catch(_){}
app.quit();
