const app = require("express")();
const express_graphql = require("express-graphql");
const { buildSchema } = require("graphql");

const schema = buildSchema(`
    type Query {
        Book(isbn: String!): Book
        Books(title: String): [Book]
    },
    type Book {
        isbn: String
        title: String
        authors: [String]
        price: Float
    }
`);

const BooksData = [
  {
    isbn: "978-111",
    title: "The REST API Design Handbook",
    authors: ["George Reese", "Christian Reilly"],
    price: 4.99
  },
  {
    isbn: "978-222",
    title: "Head First JavaScript Programming",
    authors: ["Eric Freeman", "Elisabeth Robson"],
    price: 38.97
  },
  {
    isbn: "978-333",
    title: "RESTful API Design: Best Practices in API Design with REST",
    authors: ["Matthias Biehl"],
    price: 9.99
  }
];

const getBook = args => {
  const isbn = args.isbn;
  return BooksData.filter(Book => Book.isbn === isbn)[0];
};

const getBooks = args => {
  if (args.title) {
    const title = args.title;
    return BooksData.filter(Book => Book.title.match(new RegExp(title)));
  }
  return BooksData;
};

const booksRoot = {
  Book: getBook,
  Books: getBooks
};

app.use(
  "/bookinfo",
  express_graphql({
    schema: schema,
    rootValue: booksRoot,
    graphiql: true
  })
);

app.listen(3000, () =>
  console.log("Express GraphQL Server Now Running On localhost:3000/graphql")
);
