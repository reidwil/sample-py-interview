### Notes - 2021-12-03
- This script will take our snowflake connection and upload files from our server to our target snowflake table
- [Snowflake doesn't like files of 100gb](https://docs.snowflake.com/en/user-guide/data-load-considerations-prepare.html#general-file-sizing-recommendations) so I have compressed the csvs into .gzip
- **Performance improvement**: Currently this is done on a file by file basis but should absolutely be done in parallel.
  - We can achieve that using the [Threading module](https://docs.python.org/3/library/threading.html).
  - If you have time this week, can you make a threading class that I can inhert into the Snowflake class?
- Let me know if anything catches your eye and needs addressing!