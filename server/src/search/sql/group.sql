CREATE INDEX groups_covering_index
  ON groups
  USING btree
  (type, members_count, is_closed, country, city);
