#!/usr/bin/expect

set host "photoframe"
set user "admin"
set password "password"
set remote_dir "/home/admin"
set watched_dir "/Users/jason/LocalWorkspace/photo-frame"

while {1} {
  set files [exec find $watched_dir -type f -mmin -1]
  if {[string length $files] > 0} {
    foreach file [split $files "\n"] {
      puts "Detected file change: $file"
      spawn sftp $user@$host
      expect "password:"
      send "$password\r"
      expect "sftp>"
      send "cd $remote_dir\r"
      expect "sftp>"
      send "put $file\r"
      expect "sftp>"
      send "exit\r"
      expect eof
    }
  }
  sleep 10
}