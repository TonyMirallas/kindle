
# Kindle Highlights Scraping

This project consists on the Scraping and storing of Highlights from amazon Highlights page


## Authors

- [@tonymirallas](https://github.com/TonyMirallas)


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`DATABASE`

`DB_USER`

`DB_PASSWORD`

`DB_PORT`

## API Reference

#### Get all items

```http
  GET /api/get-highlights
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `api_key` | `string` | **Required**. Your API key |

#### Get item

```http
  GET /api/get-highlight/${id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |
