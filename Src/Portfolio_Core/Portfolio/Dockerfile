#See https://aka.ms/customizecontainer to learn how to customize your debug container and how Visual Studio uses this Dockerfile to build your images for faster debugging.

FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS base
WORKDIR /app
EXPOSE 80
EXPOSE 443

FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src
COPY ["Portfolio/Portfolio.csproj", "Portfolio/"]
RUN dotnet restore "Portfolio/Portfolio.csproj"
COPY . .
WORKDIR "/src/Portfolio"
RUN dotnet build "Portfolio.csproj" -c Release -o /app/build

FROM build AS publish
RUN dotnet publish "Portfolio.csproj" -c Release -o /app/publish /p:UseAppHost=false

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "Portfolio.dll"]