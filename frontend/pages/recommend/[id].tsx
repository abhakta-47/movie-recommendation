import Head from "next/head";
import { useState, useEffect } from "react";
import { useRouter } from "next/router";

export default function Recommend() {
  let [searchKey, setSearchKey] = useState("");

  return (
    <>
      <Head>
        <title>Machine Learning by abhakta47</title>
        <link rel="icon" href="/favicon.ico" />
        {/* <meta charset="UTF-8"></meta> */}
        <meta
          name="description"
          content="Movie recommendation using ML algos, by abhakta-47"
        ></meta>
        <meta
          name="keywords"
          content="ML, ReactJs, NextJs, Classfication, regression"
        ></meta>
        <meta name="author" content="abhakta-47"></meta>
      </Head>

      <div className="m-2">
        <h1>Recommended movies :: </h1>
        <RecommendedMovies />
      </div>
    </>
  );
}

let apiKey = "00112194220384db1f4e36062ac14246";

let RecommendedMovies = () => {
  let [isLoading, setIsLoading] = useState(true);
  let [movies, setMovies] = useState([]);
  // console.log(url);
  const router = useRouter();
  const { id } = router.query;
  const url = `https://movie-rec-sys-byab47.herokuapp.com/recommendv2/${id}`;

  useEffect(() => {
    if (!router.isReady) return;
    fetch(url)
      .then((res) => res.json())
      .then(
        (res) => {
          // console.log("url", url);
          // console.log("res", res);
          if (res.status != 200) {
            console.error("error: ", res.status);
          }
          Promise.all(
            res.data.map((id) =>
              fetch(
                `https://api.themoviedb.org/3/movie/${id}?api_key=${apiKey}&language=en-US`
              )
                .then((res) => res.json())
                .catch((err) => console.error(err))
            )
          ).then((data) => {
            // console.log(data);
            setMovies(data);
          });
        },
        (err) => console.error("err", err)
      );
    setIsLoading(false);
  }, [router.isReady]);

  if (isLoading) {
    return (
      <div className="flex flex-wrap">
        <h1>loading..</h1>
      </div>
    );
  } else {
    return (
      <div className="flex flex-wrap">
        {movies
          ? movies.map((movie: any) => {
              // return <p>{movie.original_title}</p>;
              return (
                <div
                  key={movie.id}
                  className="my-1 px-1 w-full md:w-1/2 lg:my-4 lg:px-4 lg:w-1/3"
                  // style={{ "max-width": "15rem" }}
                >
                  <article className="overflow-hidden rounded-lg shadow-lg">
                    <img
                      alt="Placeholder"
                      className="block h-auto w-full"
                      src={
                        movie.poster_path
                          ? `https://www.themoviedb.org/t/p/w600_and_h900_bestv2/${movie.poster_path}`
                          : "https://plchldr.co/i/200x300?text=poster_not_found&bg=fff&fc=000"
                      }
                    ></img>

                    <header className="items-center justify-between leading-tight p-2 md:p-4">
                      <h3 className="text-lg">
                        <a
                          className="no-underline hover:underline text-black"
                          href={`https://www.themoviedb.org/movie/${movie.id}`}
                        >
                          {movie.original_title}
                        </a>
                      </h3>
                      <p className="text-grey-darker text-sm">
                        {movie.release_date}
                      </p>
                    </header>

                    <footer className="flex items-center justify-between leading-none p-2 md:p-4"></footer>
                  </article>
                </div>
              );
            })
          : ""}
      </div>
    );
  }
};
