export interface cv {
    id?: number;
    name?: string;
    birth_date?: Date;
    phone?: string;
    country?: string;
    address?: string;
    avatar?: string;
    description?: string;
    education?: education[];
    workexperience?: workexperience[];
    languages?: language[];
}

export interface education {
    name?: string;
    place?: string;
    start_date?: Date;
    end_date?: Date;
}

export interface workexperience {
    name?: string;
    ocupation?: string;
    start_date?: Date;
    end_date?: Date;
}

export interface language {
    name?: string;
}