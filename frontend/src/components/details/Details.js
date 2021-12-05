function Details(props) {
    let emptiness = []

    return(
        <div className="film-details font-style">
            <div className="poster-details">
                <img className="poster-img" src={{props.image}}/>
                <p className="ageLimit-poster">{props.ratingAgeLimits}+</p>
            </div>
            <div className="film-info">
                <div>
                    <h1>{props.name} ({props.year})</h1>
                    <h2 className="film-slogan">{props.slogan}</h2>
                </div>
                <h2>О фильме</h2>
                <p>Год выпуска: {props.year}</p>
                <div className="film-countries-genres">
                    <ul className="film-list">Страна: {props.countries?.map((с, index) => {
                        return(
                            <Link className="list-item" key={index} to={{ pathname: `/countries/${с.slug}/`}}>{с.title}</Link>
                        )
                    })}</ul>
                    <ul className="film-list">Жанр: {props.genres?.map((g, index) => {
                        return(
                            <Link className="list-item" key={index} to={{ pathname: `/genres/${g.slug}/`}}>{g.title}</Link>
                        )
                    })}</ul>
                </div>
                <p>Премьера в мире: {props.dateW}</p>
                <p>Премьера в России: {props.dateRu}</p>
                <p>Бюджет: {props.budget}</p>
                <p>Сборы в мире: ${props.grossWorld}</p>
                <p>Сборы в России: ${props.grossRu}</p>
                <p>Время: {props.filmLength}</p>
            </div>
            <div className="rating-and-actors">
                <div className="film-rating">
                    <h1>{props.rating}</h1>
                    <div className="rating-body">
                        <div className="rating-active" style={{width: `${props.rating / 0.1}%`}}></div>
                    </div>
                </div>
                <div className="film-actors">
                    <h3>В главных ролях</h3>
                    <div>
                        <ul className="actors">
                            {props.actors ? props.actors?.map((a, index) => {
                                if(index < 10)
                                    return(
                                        <div className="actors-item" key={a.id}>
                                            <p><Link key={a.id} className="actor" to={{ pathname: `/staff/${a.id}/`}}>{a.nameRu}</Link></p>
                                        </div>
                                    )}
                            ) :  emptiness.unshift("gecnj")}
                        </ul>
                        <p>{emptiness[0]}</p>
                        <Link key={props.id} id="others" to={{ pathname: `/films/${props.id}/staff`}}>Остальные персоны</Link>
                    </div>
                </div>
            </div>
        </div>
    )

}