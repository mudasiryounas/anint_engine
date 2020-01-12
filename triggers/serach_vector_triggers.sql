create or replace function app_contents_search_vector_update() returns trigger
    language plpgsql
as
$$
BEGIN
    NEW.search_vector = to_tsvector('pg_catalog.english', coalesce(substring(NEW.content, 0, 500000), ''));
    RETURN NEW;
END
$$;


create trigger app_contents_search_vector_trigger
    before insert or update
    on public.app_contents
    for each row
execute procedure app_contents_search_vector_update();
