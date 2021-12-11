import Head from "next/head";
import { useState, useEffect } from "react";

export default function Home() {
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
        <Search setSearchKey={setSearchKey} />
        <ResultMovies searchKey={searchKey} />
      </div>
    </>
  );
}

let apiKey = "00112194220384db1f4e36062ac14246";

// import React from 'react'

let Search = ({ setSearchKey }) => {
  let [localSearchKey, setLocalSearchKey] = useState("");
  const handleKeyDown = (event) => {
    if (event.key === "Enter") {
      setSearchKey(localSearchKey);
    }
  };
  return (
    <>
      <div className="flex">
        <input
          onChange={(e) => setLocalSearchKey(e.target.value)}
          onKeyDown={handleKeyDown}
          className="p-2"
          type="text"
          name=""
          id=""
          placeholder="search movies"
        />
        <button
          className="ms-2 px-2 bg-sky-500 text-white"
          onClick={(e) => setSearchKey(localSearchKey)}
        >
          search
        </button>
      </div>
    </>
  );
};

let ResultMovies = ({ searchKey }) => {
  let [movies, setMovies] = useState([{}]);

  useEffect(() => {
    let url = `https://api.themoviedb.org/3/search/movie?api_key=${apiKey}&query=${searchKey}&page=1`;
    fetch(url)
      .then((res) => res.json())
      .then(
        (res) => {
          // console.log(typeof res.results, JSON.parse(res.results));
          setMovies(res.results);
        },
        (err) => console.error(err)
      );
  }, [searchKey]);

  const handleGetRecommendation = (e) => {
    // console.log(e.target.dataset.id);
    window.location.href = `recommend/${e.target.dataset.id}`;
  };

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

                  <footer className="flex items-center justify-between leading-none p-2 md:p-4">
                    <button
                      className="ms-2 px-5 py-3 bg-sky-500 text-white"
                      data-id={movie.id}
                      onClick={handleGetRecommendation}
                    >
                      Get recommendation
                    </button>
                  </footer>
                </article>
              </div>
            );
          })
        : ""}
    </div>
  );
};
