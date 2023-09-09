from urllib.parse import urlparse


class PathRouter:
    @staticmethod
    def determine_path(request_path: str) -> str:
        """ Медод позволяет получить путь"""
        path = urlparse(request_path).path
        split_path = path.split('/')
        if len(split_path) == 2:
            route = split_path[1]
        else:
            route = split_path[1] + '/'
        return route

    @staticmethod
    def determine_path_params(request_path: str) -> tuple:
        """ Метод возвращает компоненты пути в кортеже"""
        path = urlparse(request_path).path
        path_params = tuple(path.split('/')[2:])
        return path_params
