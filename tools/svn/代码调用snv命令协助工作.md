
# 代码调用snv命令协助工作
工作中用到svn，可以把一些重复的工作用代码自动完成。比如在bug提交过程中用代码生成diff文件、提交记录等，再比如经过一段时间把一个功能合入到某个分支，现在需要把这个功能合入的到其他的分支，这两个分支不能直接merge，这时可以用代码提取出这段时间所有的提交记录，把修改的文件去重显示，然后把这些文件修改的复制到其他的分支。

## svn命令
先列举些可能用到的svn命令，代码还没写因为最近考虑离职，就先不写代码了，先把这些命令记录一下，如果以后工作中还遇到这些问题就把代码写一下，现在懒得写。

### help
不用说，就是用于查询有哪些命令可以用。
```
D:\svn\dac107>svn help
usage: svn <subcommand> [options] [args]
Subversion command-line client, version 1.8.3.
Type 'svn help <subcommand>' for help on a specific subcommand.
Type 'svn --version' to see the program version and RA modules
  or 'svn --version --quiet' to see just the version number.

Most subcommands take file and/or directory arguments, recursing
on the directories.  If no arguments are supplied to such a
command, it recurses on the current directory (inclusive) by default.

Available subcommands:
   add
   blame (praise, annotate, ann)
   cat
   changelist (cl)
   checkout (co)
   cleanup
   commit (ci)
   copy (cp)
   delete (del, remove, rm)
   diff (di)
   export
   help (?, h)
   import
   info
   list (ls)
   lock
   log
   merge
   mergeinfo
   mkdir
   move (mv, rename, ren)
   patch
   propdel (pdel, pd)
   propedit (pedit, pe)
   propget (pget, pg)
   proplist (plist, pl)
   propset (pset, ps)
   relocate
   resolve
   resolved
   revert
   status (stat, st)
   switch (sw)
   unlock
   update (up)
   upgrade

Subversion is a tool for version control.
For additional information, see http://subversion.apache.org/
```

### log
显示提交的历史记录可以显示详细的（修改了哪些文件）。

```
D:\svn\modify>svn help log
log: Show the log messages for a set of revision(s) and/or path(s).
usage: 1. log [PATH][@REV]
       2. log URL[@REV] [PATH...]

  1. Print the log messages for the URL corresponding to PATH
     (default: '.'). If specified, REV is the revision in which the
     URL is first looked up, and the default revision range is REV:1.
     If REV is not specified, the default revision range is BASE:1,
     since the URL might not exist in the HEAD revision.

  2. Print the log messages for the PATHs (default: '.') under URL.
     If specified, REV is the revision in which the URL is first
     looked up, and the default revision range is REV:1; otherwise,
     the URL is looked up in HEAD, and the default revision range is
     HEAD:1.

  Multiple '-c' or '-r' options may be specified (but not a
  combination of '-c' and '-r' options), and mixing of forward and
  reverse ranges is allowed.

  With -v, also print all affected paths with each log message.
  With -q, don't print the log message body itself (note that this is
  compatible with -v).

  Each log message is printed just once, even if more than one of the
  affected paths for that revision were explicitly requested.  Logs
  follow copy history by default.  Use --stop-on-copy to disable this
  behavior, which can be useful for determining branchpoints.

  The --depth option is only valid in combination with the --diff option
  and limits the scope of the displayed diff to the specified depth.

  If the --search option is used, log messages are displayed only if the
  provided search pattern matches any of the author, date, log message
  text (unless --quiet is used), or, if the --verbose option is also
  provided, a changed path.
  The search pattern may include "glob syntax" wildcards:
      ?      matches any single character
      *      matches a sequence of arbitrary characters
      [abc]  matches any of the characters listed inside the brackets
  If multiple --search options are provided, a log message is shown if
  it matches any of the provided search patterns. If the --search-and
  option is used, that option's argument is combined with the pattern
  from the previous --search or --search-and option, and a log message
  is shown only if it matches the combined search pattern.
  If --limit is used in combination with --search, --limit restricts the
  number of log messages searched, rather than restricting the output
  to a particular number of matching log messages.

  Examples:

    Show the latest 5 log messages for the current working copy
    directory and display paths changed in each commit:
      svn log -l 5 -v

    Show the log for bar.c as of revision 42:
      svn log bar.c@42

    Show log messages and diffs for each commit to foo.c:
      svn log --diff http://www.example.com/repo/project/foo.c
    (Because the above command uses a full URL it does not require
     a working copy.)

    Show log messages for the children foo.c and bar.c of the directory
    '/trunk' as it appeared in revision 50, using the ^/ URL shortcut:
      svn log ^/trunk@50 foo.c bar.c

    Show the log messages for any incoming changes to foo.c during the
    next 'svn update':
      svn log -r BASE:HEAD foo.c

    Show the log message for the revision in which /branches/foo
    was created:
      svn log --stop-on-copy --limit 1 -r0:HEAD ^/branches/foo

Valid options:
  -r [--revision] ARG      : ARG (some commands also take ARG1:ARG2 range)
                             A revision argument can be one of:
                                NUMBER       revision number
                                '{' DATE '}' revision at start of the date
                                'HEAD'       latest in repository
                                'BASE'       base rev of item's working copy
                                'COMMITTED'  last commit at or before BASE
                                'PREV'       revision just before COMMITTED
  -q [--quiet]             : print nothing, or only summary information
  -v [--verbose]           : print extra information
  -g [--use-merge-history] : use/display additional information from merge
                             history
  -c [--change] ARG        : the change made in revision ARG
  --targets ARG            : pass contents of file ARG as additional args
  --stop-on-copy           : do not cross copies while traversing history
  --incremental            : give output suitable for concatenation
  --xml                    : output in XML
  -l [--limit] ARG         : maximum number of log entries
  --with-all-revprops      : retrieve all revision properties
  --with-no-revprops       : retrieve no revision properties
  --with-revprop ARG       : retrieve revision property ARG
  --depth ARG              : limit operation by depth ARG ('empty', 'files',
                             'immediates', or 'infinity')
  --diff                   : produce diff output
  --diff-cmd ARG           : use ARG as diff command
  --internal-diff          : override diff-cmd specified in config file
  -x [--extensions] ARG    : Specify differencing options for external diff or
                             internal diff or blame. Default: '-u'. Options are
                             separated by spaces. Internal diff and blame take:
                               -u, --unified: Show 3 lines of unified context
                               -b, --ignore-space-change: Ignore changes in
                                 amount of white space
                               -w, --ignore-all-space: Ignore all white space
                               --ignore-eol-style: Ignore changes in EOL style
                               -p, --show-c-function: Show C function name
  --search ARG             : use ARG as search pattern (glob syntax)
  --search-and ARG         : combine ARG with the previous search pattern

Global options:
  --username ARG           : specify a username ARG
  --password ARG           : specify a password ARG
  --no-auth-cache          : do not cache authentication tokens
  --non-interactive        : do no interactive prompting (default is to prompt
                             only if standard input is a terminal device)
  --force-interactive      : do interactive prompting even if standard input
                             is not a terminal device
  --trust-server-cert      : accept SSL server certificates from unknown
                             certificate authorities without prompting (but only
                             with '--non-interactive')
  --config-dir ARG         : read user configuration files from directory ARG
  --config-option ARG      : set user configuration option in the format:
                                 FILE:SECTION:OPTION=[VALUE]
                             For example:
                                 servers:global:http-library=serf


```

#### 显示提交记录
可以指定路径，不指定的话，就是作用于在当前路径check出的svn工程。

`-l`用于限制输出的记录数，默认会很多。

```
D:\svn\dac107>svn log svn://192.168.6.54/dptech/UMCV5.3/branches/5.3.22/dev_dac_newpage -l 3
------------------------------------------------------------------------
r40069 | lifengchao | 2020-07-31 11:03:23 +0800 (周五, 31 七月 2020) | 1 line

修改厂商回显，定时器冲突
------------------------------------------------------------------------
r40058 | zhangying | 2020-07-30 18:45:59 +0800 (周四, 30 七月 2020) | 1 line

知识库功能sql文件提交
------------------------------------------------------------------------
r40057 | zhangying | 2020-07-30 18:40:26 +0800 (周四, 30 七月 2020) | 1 line

工单功能c++提交
------------------------------------------------------------------------

```

#### 带修改文件信息
加个`-v`就行

```
D:\svn\dac107>svn log svn://192.168.6.54/dptech/UMCV5.3/branches/5.3.22/dev_dac_newpage -l 3 -v
------------------------------------------------------------------------
r40069 | lifengchao | 2020-07-31 11:03:23 +0800 (周五, 31 七月 2020) | 1 line
Changed paths:
   M /dptech/UMCV5.3/branches/5.3.22/dev_dac_newpage/dp/WebRoot/dac/dacAssetManageTerm.jsp
   M /dptech/UMCV5.3/branches/5.3.22/dev_dac_newpage/dp/WebRoot/dac/sub/dacAssetManageTermAddInfoFromScan.jsp
   M /dptech/UMCV5.3/branches/5.3.22/dev_dac_newpage/dp/WebRoot/dac/sub/dacAssetManageTermEditInfo.jsp

修改厂商回显，定时器冲突
------------------------------------------------------------------------
r40058 | zhangying | 2020-07-30 18:45:59 +0800 (周四, 30 七月 2020) | 1 line
Changed paths:
   M /dptech/UMCV5.3/branches/5.3.22/dev_dac_newpage/UMC/dbscript/V05R03B022D00.sql

知识库功能sql文件提交
------------------------------------------------------------------------
r40057 | zhangying | 2020-07-30 18:40:26 +0800 (周四, 30 七月 2020) | 1 line
Changed paths:
   M /dptech/UMCV5.3/branches/5.3.22/dev_dac_newpage/daemon/DaemonService/UMCDaemon/UMCDaemon.vcproj
   M /dptech/UMCV5.3/branches/5.3.22/dev_dac_newpage/daemon/DaemonService/UMCDaemon/filestore/filestoredef_loader.cpp
   M /dptech/UMCV5.3/branches/5.3.22/dev_dac_newpage/daemon/DaemonService/UMCDaemon/filestore/filestoredef_loader.h
   M /dptech/UMCV5.3/branches/5.3.22/dev_dac_newpage/daemon/DaemonService/UMCDaemon/filestore/filestoredef_log.cpp
   M /dptech/UMCV5.3/branches/5.3.22/dev_dac_newpage/daemon/DaemonService/UMCDaemon/filestore/filestoredef_query.cpp
   M /dptech/UMCV5.3/branches/5.3.22/dev_dac_newpage/daemon/DaemonService/UMCDaemon/mod_dac/dac_dynamicperceivelog.cpp
   M /dptech/UMCV5.3/branches/5.3.22/dev_dac_newpage/daemon/DaemonService/UMCDaemon/mod_dac/dac_dynamicperceivelog.h
   M /dptech/UMCV5.3/branches/5.3.22/dev_dac_newpage/daemon/DaemonService/UMCDaemon/mod_dac/dac_dynamicperceivelogdetail.cpp
   M /dptech/UMCV5.3/branches/5.3.22/dev_dac_newpage/daemon/DaemonService/UMCDaemon/mod_dac/dac_dynamicperceivelogdetail.h
   A /dptech/UMCV5.3/branches/5.3.22/dev_dac_newpage/daemon/DaemonService/UMCDaemon/mod_dac/dac_hp_logOverview_StatisByIpAndLogType.cpp
   A /dptech/UMCV5.3/branches/5.3.22/dev_dac_newpage/daemon/DaemonService/UMCDaemon/mod_dac/dac_hp_logOverview_StatisByIpAndLogType.h
   A /dptech/UMCV5.3/branches/5.3.22/dev_dac_newpage/daemon/DaemonService/UMCDaemon/mod_dac/dac_hp_logOverview_StatisByLogType.cpp
   A /dptech/UMCV5.3/branches/5.3.22/dev_dac_newpage/daemon/DaemonService/UMCDaemon/mod_dac/dac_hp_logOverview_StatisByLogType.h
   A /dptech/UMCV5.3/branches/5.3.22/dev_dac_newpage/daemon/DaemonService/UMCDaemon/mod_dac/dac_hp_logOverview_StatisByLogTypeAndTermType.cpp
   A /dptech/UMCV5.3/branches/5.3.22/dev_dac_newpage/daemon/DaemonService/UMCDaemon/mod_dac/dac_hp_logOverview_StatisByLogTypeAndTermType.h
   A /dptech/UMCV5.3/branches/5.3.22/dev_dac_newpage/daemon/DaemonService/UMCDaemon/mod_dac/dac_hp_logOverview_ip_warn_topn.cpp
   A /dptech/UMCV5.3/branches/5.3.22/dev_dac_newpage/daemon/DaemonService/UMCDaemon/mod_dac/dac_hp_logOverview_ip_warn_topn.h
   A /dptech/UMCV5.3/branches/5.3.22/dev_dac_newpage/daemon/DaemonService/UMCDaemon/mod_dac/dac_hp_logOverview_relationMapByLogTypeAndDev.cpp
   A /dptech/UMCV5.3/branches/5.3.22/dev_dac_newpage/daemon/DaemonService/UMCDaemon/mod_dac/dac_hp_logOverview_relationMapByLogTypeAndDev.h
   A /dptech/UMCV5.3/branches/5.3.22/dev_dac_newpage/daemon/DaemonService/UMCDaemon/mod_dac/dac_hp_worklist_process.cpp
   A /dptech/UMCV5.3/branches/5.3.22/dev_dac_newpage/daemon/DaemonService/UMCDaemon/mod_dac/dac_hp_worklist_process.h
   M /dptech/UMCV5.3/branches/5.3.22/dev_dac_newpage/daemon/DaemonService/UMCDaemon/mod_dac/dac_ipgroup.cpp
   M /dptech/UMCV5.3/branches/5.3.22/dev_dac_newpage/daemon/DaemonService/UMCDaemon/mod_dac/dac_ipgroup.h
   M /dptech/UMCV5.3/branches/5.3.22/dev_dac_newpage/daemon/DaemonService/UMCDaemon/mod_dac/dac_logOverviewHandle.cpp
   M /dptech/UMCV5.3/branches/5.3.22/dev_dac_newpage/daemon/DaemonService/UMCDaemon/mod_dac/dac_logOverviewHandle.h
   A /dptech/UMCV5.3/branches/5.3.22/dev_dac_newpage/daemon/DaemonService/UMCDaemon/mod_dac/dac_sysgradecfg.cpp
   A /dptech/UMCV5.3/branches/5.3.22/dev_dac_newpage/daemon/DaemonService/UMCDaemon/mod_dac/dac_sysgradecfg.h
   M /dptech/UMCV5.3/branches/5.3.22/dev_dac_newpage/daemon/DaemonService/UMCDaemon/mod_dac/mod_dac.cpp
   M /dptech/UMCV5.3/branches/5.3.22/dev_dac_newpage/daemon/DaemonService/UMCDaemon/mod_dac/mod_dac.h
   A /dptech/UMCV5.3/branches/5.3.22/dev_dac_newpage/daemon/DaemonService/UMCDaemon/mod_dac/query_hp_worklist_group_by_day.cpp
   A /dptech/UMCV5.3/branches/5.3.22/dev_dac_newpage/daemon/DaemonService/UMCDaemon/mod_dac/query_hp_worklist_group_by_day.h
   A /dptech/UMCV5.3/branches/5.3.22/dev_dac_newpage/daemon/DaemonService/UMCDaemon/mod_dac/query_hp_worklist_group_by_handle_status.cpp
   A /dptech/UMCV5.3/branches/5.3.22/dev_dac_newpage/daemon/DaemonService/UMCDaemon/mod_dac/query_hp_worklist_group_by_handle_status.h
   A /dptech/UMCV5.3/branches/5.3.22/dev_dac_newpage/daemon/DaemonService/UMCDaemon/mod_dac/query_hp_worklist_group_by_node_id.cpp
   A /dptech/UMCV5.3/branches/5.3.22/dev_dac_newpage/daemon/DaemonService/UMCDaemon/mod_dac/query_hp_worklist_group_by_node_id.h
   A /dptech/UMCV5.3/branches/5.3.22/dev_dac_newpage/daemon/DaemonService/UMCDaemon/mod_dac/query_hp_worklist_group_by_overtime.cpp
   A /dptech/UMCV5.3/branches/5.3.22/dev_dac_newpage/daemon/DaemonService/UMCDaemon/mod_dac/query_hp_worklist_group_by_overtime.h
   A /dptech/UMCV5.3/branches/5.3.22/dev_dac_newpage/daemon/DaemonService/UMCDaemon/mod_dac/query_hp_worklist_group_by_terminal_type.cpp
   A /dptech/UMCV5.3/branches/5.3.22/dev_dac_newpage/daemon/DaemonService/UMCDaemon/mod_dac/query_hp_worklist_group_by_terminal_type.h
   A /dptech/UMCV5.3/branches/5.3.22/dev_dac_newpage/daemon/DaemonService/UMCDaemon/mod_dac/query_hp_worklist_process_detail.cpp
   A /dptech/UMCV5.3/branches/5.3.22/dev_dac_newpage/daemon/DaemonService/UMCDaemon/mod_dac/query_hp_worklist_process_detail.h
   A /dptech/UMCV5.3/branches/5.3.22/dev_dac_newpage/daemon/DaemonService/UMCDaemon/mod_dac/query_hp_worklist_process_operate_detail.cpp
   A /dptech/UMCV5.3/branches/5.3.22/dev_dac_newpage/daemon/DaemonService/UMCDaemon/mod_dac/query_hp_worklist_process_operate_detail.h
   M /dptech/UMCV5.3/branches/5.3.22/dev_dac_newpage/daemon/DaemonService/UMCDaemon/mod_sys/sys_gradereg.cpp
   M /dptech/UMCV5.3/branches/5.3.22/dev_dac_newpage/daemon/DaemonService/UMCDaemon/mod_sys/sys_gradereg.h
   M /dptech/UMCV5.3/branches/5.3.22/dev_dac_newpage/daemon/DaemonService/UMCDaemon/receiver/recv3.cpp
   M /dptech/UMCV5.3/branches/5.3.22/dev_dac_newpage/daemon/DaemonService/UMCDaemon/receiver/uagns/uagns_recv.cpp
   M /dptech/UMCV5.3/branches/5.3.22/dev_dac_newpage/daemon/DaemonService/UMCDaemon/util/util.h
   M /dptech/UMCV5.3/branches/5.3.22/dev_dac_newpage/daemon/DaemonService/libpub/logst.h
   M /dptech/UMCV5.3/branches/5.3.22/dev_dac_newpage/daemon/DaemonService/libpub/queryid.h
   M /dptech/UMCV5.3/branches/5.3.22/dev_dac_newpage/daemon/DaemonService/libpub/queryst.h

工单功能c++提交
------------------------------------------------------------------------

```

### diff
显示某次提交记录的修改详细信息，这个可以用于流程中的修改阶段.diff。

```
D:\svn\dac107>svn help diff
diff (di): Display local changes or differences between two revisions or paths.
usage: 1. diff
       2. diff [-c M | -r N[:M]] [TARGET[@REV]...]
       3. diff [-r N[:M]] --old=OLD-TGT[@OLDREV] [--new=NEW-TGT[@NEWREV]] \
               [PATH...]
       4. diff OLD-URL[@OLDREV] NEW-URL[@NEWREV]
       5. diff OLD-URL[@OLDREV] NEW-PATH[@NEWREV]
       6. diff OLD-PATH[@OLDREV] NEW-URL[@NEWREV]

  1. Use just 'svn diff' to display local modifications in a working copy.

  2. Display the changes made to TARGETs as they are seen in REV between
     two revisions.  TARGETs may be all working copy paths or all URLs.
     If TARGETs are working copy paths, N defaults to BASE and M to the
     working copy; if URLs, N must be specified and M defaults to HEAD.
     The '-c M' option is equivalent to '-r N:M' where N = M-1.
     Using '-c -M' does the reverse: '-r M:N' where N = M-1.

  3. Display the differences between OLD-TGT as it was seen in OLDREV and
     NEW-TGT as it was seen in NEWREV.  PATHs, if given, are relative to
     OLD-TGT and NEW-TGT and restrict the output to differences for those
     paths.  OLD-TGT and NEW-TGT may be working copy paths or URL[@REV].
     NEW-TGT defaults to OLD-TGT if not specified.  -r N makes OLDREV default
     to N, -r N:M makes OLDREV default to N and NEWREV default to M.
     If OLDREV or NEWREV are not specified, they default to WORKING for
     working copy targets and to HEAD for URL targets.

     Either or both OLD-TGT and NEW-TGT may also be paths to unversioned
     targets. Revisions cannot be specified for unversioned targets.
     Both targets must be of the same node kind (file or directory).
     Diffing unversioned targets against URL targets is not supported.

  4. Shorthand for 'svn diff --old=OLD-URL[@OLDREV] --new=NEW-URL[@NEWREV]'
  5. Shorthand for 'svn diff --old=OLD-URL[@OLDREV] --new=NEW-PATH[@NEWREV]'
  6. Shorthand for 'svn diff --old=OLD-PATH[@OLDREV] --new=NEW-URL[@NEWREV]'

Valid options:
  -r [--revision] ARG      : ARG (some commands also take ARG1:ARG2 range)
                             A revision argument can be one of:
                                NUMBER       revision number
                                '{' DATE '}' revision at start of the date
                                'HEAD'       latest in repository
                                'BASE'       base rev of item's working copy
                                'COMMITTED'  last commit at or before BASE
                                'PREV'       revision just before COMMITTED
  -c [--change] ARG        : the change made by revision ARG (like -r ARG-1:ARG)
                             If ARG is negative this is like -r ARG:ARG-1
                             If ARG is of the form ARG1-ARG2 then this is like
                             ARG1:ARG2, where ARG1 is inclusive
  --old ARG                : use ARG as the older target
  --new ARG                : use ARG as the newer target
  -N [--non-recursive]     : obsolete; try --depth=files or --depth=immediates
  --depth ARG              : limit operation by depth ARG ('empty', 'files',
                             'immediates', or 'infinity')
  --diff-cmd ARG           : use ARG as diff command
  --internal-diff          : override diff-cmd specified in config file
  -x [--extensions] ARG    : Specify differencing options for external diff or
                             internal diff or blame. Default: '-u'. Options are
                             separated by spaces. Internal diff and blame take:
                               -u, --unified: Show 3 lines of unified context
                               -b, --ignore-space-change: Ignore changes in
                                 amount of white space
                               -w, --ignore-all-space: Ignore all white space
                               --ignore-eol-style: Ignore changes in EOL style
                               -p, --show-c-function: Show C function name
  --no-diff-added          : do not print differences for added files
  --no-diff-deleted        : do not print differences for deleted files
  --ignore-properties      : ignore properties during the operation
  --properties-only        : show only properties during the operation
  --show-copies-as-adds    : don't diff copied or moved files with their source
  --notice-ancestry        : diff unrelated nodes as delete and add
  --summarize              : show a summary of the results
  --changelist [--cl] ARG  : operate only on members of changelist ARG
  --force                  : force operation to run
  --xml                    : output in XML
  --git                    : use git's extended diff format
  --patch-compatible       : generate diff suitable for generic third-party
                             patch tools; currently the same as
                             --show-copies-as-adds --ignore-properties

Global options:
  --username ARG           : specify a username ARG
  --password ARG           : specify a password ARG
  --no-auth-cache          : do not cache authentication tokens
  --non-interactive        : do no interactive prompting (default is to prompt
                             only if standard input is a terminal device)
  --force-interactive      : do interactive prompting even if standard input
                             is not a terminal device
  --trust-server-cert      : accept SSL server certificates from unknown
                             certificate authorities without prompting (but only
                             with '--non-interactive')
  --config-dir ARG         : read user configuration files from directory ARG
  --config-option ARG      : set user configuration option in the format:
                                 FILE:SECTION:OPTION=[VALUE]
                             For example:
                                 servers:global:http-library=serf

```

通过log命令最新的两条记录，比较他们的不同
```
D:\svn\dac107>svn diff  -r 40069:40058 svn://192.168.6.54/dptech/UMCV5.3/branches/5.3.22/dev_dac_newpage
Index: dp/WebRoot/dac/dacAssetManageTerm.jsp
===================================================================
--- dp/WebRoot/dac/dacAssetManageTerm.jsp       (revision 40069)
+++ dp/WebRoot/dac/dacAssetManageTerm.jsp       (revision 40058)
@@ -1205,9 +1205,9 @@
                     return a[1].order - b[1].order;
                 });

-                if(this._loopTimerT !== undefined){
-                       clearTimeout(this._loopTimerT);
-                       this._loopTimerT = undefined;
+                if(this._timerT !== undefined){
+                       clearTimeout(this._timerT);
+                       this._timerT = undefined;
                 }
                 var showDatas = datas.filter(function(e){return e.count>0;});
                 if(showDatas.length > centers.length){
@@ -1221,7 +1221,7 @@
                                this.showStartIndex = 0;
                        }
                        var self = this;
-                       this._loopTimerT = setTimeout(function () {
+                       this._timerT = setTimeout(function () {
                                self.drawEchartScatter_termType(self.datas);
                     }, 5000);
                 }else{
Index: dp/WebRoot/dac/sub/dacAssetManageTermAddInfoFromScan.jsp
===================================================================
--- dp/WebRoot/dac/sub/dacAssetManageTermAddInfoFromScan.jsp    (revision 40069)
+++ dp/WebRoot/dac/sub/dacAssetManageTermAddInfoFromScan.jsp    (revision 40058)
@@ -853,7 +853,7 @@
        renderTo: "searchComboBox_termFactory",
        hiddenField:$("#termFactory")[0],
         width: 188,
-        value:"<s:property value='termInfoParam.factory'/>",
+        value:"澶у崕",
         store: new Ext.data.ArrayStore({
                fields: ['id', 'value'],
                data : termFactoryList_data
Index: dp/WebRoot/dac/sub/dacAssetManageTermEditInfo.jsp
===================================================================
--- dp/WebRoot/dac/sub/dacAssetManageTermEditInfo.jsp   (revision 40069)
+++ dp/WebRoot/dac/sub/dacAssetManageTermEditInfo.jsp   (revision 40058)
@@ -853,7 +853,7 @@
        renderTo: "searchComboBox_termFactory",
        hiddenField:$("#termFactory")[0],
         width: 188,
-        value:"<s:property value='termInfoParam.factory'/>",
+        value:"澶у崕",
         store: new Ext.data.ArrayStore({
                fields: ['id', 'value'],
                data : termFactoryList_data
```

通过log命令最新的一条条记录，比较这个版本号和-1的版本号似乎也是一样的，我看svn图形化工具似乎就是这样比较的
```
D:\svn\dac107>svn diff  -r 40069:40068 svn://192.168.6.54/dptech/UMCV5.3/branches/5.3.22/dev_dac_newpage
Index: dp/WebRoot/dac/sub/dacAssetManageTermAddInfoFromScan.jsp
===================================================================
--- dp/WebRoot/dac/sub/dacAssetManageTermAddInfoFromScan.jsp    (revision 40069)
+++ dp/WebRoot/dac/sub/dacAssetManageTermAddInfoFromScan.jsp    (revision 40068)
@@ -853,7 +853,7 @@
        renderTo: "searchComboBox_termFactory",
        hiddenField:$("#termFactory")[0],
         width: 188,
-        value:"<s:property value='termInfoParam.factory'/>",
+        value:"澶у崕",
         store: new Ext.data.ArrayStore({
                fields: ['id', 'value'],
                data : termFactoryList_data
Index: dp/WebRoot/dac/sub/dacAssetManageTermEditInfo.jsp
===================================================================
--- dp/WebRoot/dac/sub/dacAssetManageTermEditInfo.jsp   (revision 40069)
+++ dp/WebRoot/dac/sub/dacAssetManageTermEditInfo.jsp   (revision 40068)
@@ -853,7 +853,7 @@
        renderTo: "searchComboBox_termFactory",
        hiddenField:$("#termFactory")[0],
         width: 188,
-        value:"<s:property value='termInfoParam.factory'/>",
+        value:"澶у崕",
         store: new Ext.data.ArrayStore({
                fields: ['id', 'value'],
                data : termFactoryList_data
Index: dp/WebRoot/dac/dacAssetManageTerm.jsp
===================================================================
--- dp/WebRoot/dac/dacAssetManageTerm.jsp       (revision 40069)
+++ dp/WebRoot/dac/dacAssetManageTerm.jsp       (revision 40068)
@@ -1205,9 +1205,9 @@
                     return a[1].order - b[1].order;
                 });

-                if(this._loopTimerT !== undefined){
-                       clearTimeout(this._loopTimerT);
-                       this._loopTimerT = undefined;
+                if(this._timerT !== undefined){
+                       clearTimeout(this._timerT);
+                       this._timerT = undefined;
                 }
                 var showDatas = datas.filter(function(e){return e.count>0;});
                 if(showDatas.length > centers.length){
@@ -1221,7 +1221,7 @@
                                this.showStartIndex = 0;
                        }
                        var self = this;
-                       this._loopTimerT = setTimeout(function () {
+                       this._timerT = setTimeout(function () {
                                self.drawEchartScatter_termType(self.datas);
                     }, 5000);
                 }else{

```






```

```