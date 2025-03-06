"use server";
// graphql_query: any, graphql_variables: any=undefined, access_token: string=""
export async function graphqlRequest({
    graphql_query,
    graphql_variables=undefined,
    access_token="",
}: {
    graphql_query: string,
    graphql_variables?: any
    access_token?: string,
}): Promise<any> | null {
    const requestHeaders = new Headers();
    requestHeaders.append("Content-Type", "application/json");
    if(access_token) {
        requestHeaders.append("Authorization", `Bearer ${access_token}`);
    }
    const requestBody = JSON.stringify({query: graphql_query, variables: graphql_variables});
    console.log("REQUEST BODY", requestBody);

    const requestOptions = {
        method: "POST",
        headers: requestHeaders,
        body: requestBody
    }
    const response = await fetch(`${process.env.API_BASE_URL}/api/graphql`, requestOptions)
        .then((response) => response)
        .catch((error) => console.error(error))

    if(response && response.ok) {
        const data = await response.json();
        console.log(data);
        return data;
    }
    console.log("FAIL");
    return null
}
