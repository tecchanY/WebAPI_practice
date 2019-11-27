const app = require("express")();
const express_graphql = require("express-graphql");
const { buildSchema } = require("graphql");

// リソースのスキーマ定義
const schema = buildSchema(`
        type Query {
            message: String
        }
    `);

// リソース･オブジェクト
const msgRoot = {
  message: () => "Hello GraphQL!"
};

app.use(
  "/graphql",
  express_graphql({
    schema: schema,
    rootValue: msgRoot,
    graphiql: true
  })
);

app.listen(3000, () =>
  console.log("Express GraphQL Server Now Running On localhost:3000/graphql")
);
