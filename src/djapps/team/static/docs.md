# Team Management GraphQL API

Welcome to the Team Management GraphQL API!  
This API provides a flexible interface for managing sports teams, squads, players, coaches, leagues, tournaments, venues, and matches.

---

## Features

- **CRUD operations** for all major entities
- **GraphQL endpoint** for flexible queries and mutations
- **Pagination, filtering, and ordering**
- **Rich type system** using Strawberry GraphQL

---

## Getting Started

1. Visit the `/graphql` endpoint in your browser to access the GraphQL Playground.
2. Use the playground to explore the schema and run queries/mutations.

---

## Example Query

```graphql
{
  squads {
    id
    name
    size
    league {
      name
    }
  }
}
```

---

## Main Types

- **Squad**
- **Player**
- **Coach**
- **League**
- **Tournament**
- **Venue**
- **Match**

---

## Contact

For questions or support, contact the API maintainer.
